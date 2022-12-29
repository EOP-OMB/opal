import json
import urllib.request
import logging

from celery import Celery
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalog.models import available_catalog_list, catalogs, controls
from common.models import metadata
from component.models import components, control_implementations, implemented_requirements
from ctrl_profile.models import imports, profiles


# Create your views here.

def catalog_index_view(request):
    imported_catalogs = catalogs.objects.all()
    html_str = "<table class='table table-striped'>"
    html_str += "<tr><th>Name</th><th>Controls</th><th>Enhancements</th><th>Total</th></tr>"
    for catalog in imported_catalogs:
        html_str += "<tr>" + catalog.count_controls() + "</tr>"
    html_str += "</table>"
    logger = logging.getLogger("django")
    logger.info(html_str)
    context = {
        'title': "Catalogs",
        'content': html_str
        }
    return render(request, "generic_template.html", context)


class catalog_list_view(ListView):
    model = catalogs
    context_object_name = "context_list"
    template_name = "generic_list.html"


class catalog_detail_view(DetailView):
    model = catalogs
    context_object_name = "context"
    template_name = "generic_detail.html"


class control_detail_view(DetailView):
    model = controls
    context_object_name = "context"
    template_name = "generic_detail.html"


app = Celery('tasks', broker=settings.BROKER)


@app.task(bind=True)
def import_catalog_task(self, item=False, host=False, test=False):
    logger = logging.getLogger('django')
    if test:
        catalog_file = "sample_data/basic-catalog.json"
        catalog_json = json.load(open(catalog_file))
        catalog_dict = catalog_json["catalog"]
    else:
        if item:
            catalog_dict = download_catalog(item['link'])
        else:
            raise TypeError("You must provide a catalog to import")

    new_catalog = catalogs()
    new_catalog = new_catalog.import_oscal(catalog_dict)
    new_catalog.save()
    # create a new profile for the imported catalog
    new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
    new_profile = profiles.objects.create(
        metadata=new_metadata
        )
    new_profile.save()
    if not host:
        host = settings.HOST_NAME
    url = "https://" + host + new_catalog.get_permalink()
    new_profile.imports.add(imports.objects.create(href=url, import_type="catalog"))
    new_profile.save()
    # create components for any groups in the catalog
    for group in new_catalog.groups.all():
        new_component, created = components.objects.get_or_create(
            type="policy", title=group.title + " Policy",
            description="This Component Policy was automatically created during the import of " + new_metadata.title,
            purpose="This Component Policy was automatically created during the import of " + new_metadata.title,
            status="under-development"
            )
        if created:
            new_component.save()
    # Create implemented_requirement objects for all controls in the import
    logger.info("Creating implemented_requirement objects for all controls in the import")
    ctrl_list = new_catalog.list_all_controls()
    for ctrl in ctrl_list:
        implemented_requirements.objects.get_or_create(control_id=ctrl)
        ctrl.sort_id = ctrl._get_sort_id()
        ctrl.save()
    return new_catalog


def download_catalog(link):
    proxies = {}
    if settings.HTTP_PROXY:
        proxies['http'] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        proxies['https'] = settings.HTTPS_PROXY
    urllib.request.ProxyHandler()
    try:
        f = urllib.request.urlopen(link)
    except Exception:
        raise ConnectionError("Unable to download catalog from %s. Check that the site is accessible and your proxies are properly configured." % link)
    catalog_json = json.loads(f.read())
    catalog_dict = catalog_json["catalog"]
    return catalog_dict


def import_catalog_view(request, catalog_id):
    """
    Imports a pre-defined set of catalogs
    """
    logger = logging.getLogger('django')
    host = request.get_host()
    if available_catalog_list.objects.filter(id=catalog_id).exists:
        import_catalog_target = available_catalog_list.objects.get(id=catalog_id)
        if catalogs.objects.filter(uuid=import_catalog_target.catalog_uuid).exists():
            logger.info("Catalog with UUID %s already exists" % import_catalog_target.catalog_uuid)
        else:
            if settings.ASYNC:
                import_catalog_task.delay(import_catalog_target.__dict__, host)
            else:
                import_catalog_task(import_catalog_target.__dict__, host)
    return HttpResponseRedirect(reverse('home_page'))


def load_controls(request):
    catalog_id = request.GET.get('catalog')
    if catalogs.objects.filter(pk=catalog_id).exists():
        selected_catalog = catalogs.objects.get(pk=catalog_id)
        available_controls = []
        for ctrl in selected_catalog.list_all_controls():
            available_controls.append({"value": ctrl.id, "display": ctrl.__str__})
        return render(request, 'generic_dropdown_list_options.html', {'options': available_controls})
    else:
        return render(request, 'generic_dropdown_list_options.html', {'options': ["Invalid catalog selected, try again"]})


def load_statements(request):
    control_id = request.GET.get('control')
    statement_list = get_statements(control_id)

    return render(request, 'generic_checkbox_list_options.html', {'options': statement_list})


def load_params(request):
    control_id = request.GET.get('control')
    param_table = get_parameters(control_id)
    return render(request, 'generic_html_helper.html', {'content': param_table})


def get_statements(control_id):
    if controls.objects.filter(pk=control_id).exists():
        selected_control = controls.objects.get(pk=control_id)
        statement_list = []
        for stmt in selected_control.get_all_parts():
            if stmt.name in ["item", "statement"]:
                display_str = ""
                if len(stmt.props.filter(name="label")) > 0:
                    display_str += stmt.props.get(name="label").value + " "
                display_str += stmt.prose
                if len(display_str) > 0:
                    statement_list.append({"value": stmt.id, "display": display_str, "name": "statements"})
        return statement_list
    else:
        return ["Invalid control selected, Try again"]


def get_parameters(control_id):
    if controls.objects.filter(pk=control_id).exists():
        selected_control = controls.objects.get(pk=control_id)
        parameter_list = selected_control.params.all()
        html_str = "<table class='table-bordered'>"
        html_str += "<tr><th>Guidance</th><th>Param ID</th><th>Value</th></tr>"
        for p in parameter_list:
            html_str += p.get_form()
        html_str += "</table>"
        return html_str
    else:
        return []
