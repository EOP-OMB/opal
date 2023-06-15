from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from component.models import components
from .forms import components_form


def component_list_view(request):
    component_list = components.objects.all()
    html_str = "<table class='table primary'><tr><th>Title</th><th>Status</th><th>Controls</th></tr>"
    for comp in component_list:
        ctrl_list = comp.list_implemented_controls()
        html_ctrl_list = []
        for ctrl in ctrl_list:
            html_ctrl_list.append("<a href='%s' target='_blank'>%s</a>" % (ctrl.get_absolute_url(), ctrl.control_id))
        html_str += "<tr><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>" % (comp.get_absolute_url(),comp.title, comp.status, ', '.join(html_ctrl_list))
    context = {
        'content': html_str,
        'title': 'Component List'
    }
    return render(request, "generic_template.html", context)


class component_detail_view(DetailView):
    model = components
    context_object_name = "context"
    template_name = "generic_detail.html"


def component_workflow_view():
    html_str = "<h1>Steps to create a Component</h1>"
    html_str += "<ol><li>Create the component</li>"
    html_str += "<li>Create a control_implementations</li>"
    html_str += "<li>Add the controls</li></ol>"
    return html_str


def components_form_view(request):
    context = {}
    form = components_form(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, "generic_form.html", context)
