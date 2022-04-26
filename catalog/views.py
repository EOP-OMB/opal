import json
import requests
from opal.settings import HTTP_PROXY, HTTPS_PROXY

from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalog.models import *
from component_definition.models import components
from control_profile.models import imports, profile


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


def import_catalog_view(request, catalog_link):
    """
    Imports a pre-defined set of catalogs
    """
    from common.views import available_catalog_list

    proxies = {}
    if HTTP_PROXY:
        proxies['http'] = HTTP_PROXY
    if HTTPS_PROXY:
        proxies['https'] = HTTPS_PROXY

    for item in available_catalog_list:
        if catalog_link == item["slug"] and not catalogs.objects.filter(uuid=item['uuid']).exists():
            catalog_url = item["link"]
            f = requests.get(catalog_url, proxies=proxies)
            catalog_json = json.loads(f.text)
            catalog_dict = catalog_json["catalog"]
            new_catalog = catalogs()
            new_catalog.import_oscal(catalog_dict)
            new_catalog.save()

            # create a new profile for the imported catalog
            new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
            new_profile = profile.objects.create(
                metadata=new_metadata
                )
            new_profile.save()
            url = "https://" + request.get_host() + new_catalog.get_permalink()
            new_profile.imports.add(imports.objects.create(href=url, import_type="catalog"))
            new_profile.save()

            # create components for any groups in the catalog
            for group in new_catalog.groups.all():
                new_component = components.objects.get_or_create(
                    type="policy", title=group.title + " Policy",
                    description="This Component Policy was automatically created durring the import of " + new_metadata.title,
                    purpose="This Component Policy was automatically created durring the import of " + new_metadata.title,
                    status="under-development"
                    )

            context = {
                'msg': new_catalog.metadata.title + " imported from " + catalog_url
                }  # return render(request, "index.html", context)
    return redirect('home_page')


def load_controls(request):
    catalog_id = request.GET.get('catalog')
    selected_catalog = catalogs.objects.get(pk=catalog_id)
    available_controls = []
    for ctrl in selected_catalog.list_all_controls():
        available_controls.append({"value": ctrl.id, "display": ctrl.__str__})
    return render(request, 'generic_dropdown_list_options.html', {'options': available_controls})


def load_statements(request):
    logger = logging.getLogger('django')
    control_id = request.GET.get('control')
    statement_list = get_statments(control_id)

    return render(request, 'generic_checkbox_list_options.html', {'options': statement_list})


def get_statments(control_id):
    selected_control = controls.objects.get(pk=control_id)
    statement_list = []
    for stmt in selected_control.get_all_parts():
        if stmt.name in ["item", "statement"]:
            display_str = ""
            if len(stmt.props.filter(name="label")) > 0:
                display_str += stmt.props.get(name="label").value + " "
            display_str += stmt.prose
            if len(display_str) > 0:
                statement_list.append({"value": stmt.id, "display": display_str})
    return statement_list
