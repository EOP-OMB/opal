from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from component.models import components
from .forms import components_form


# class component_list_view(ListView):
#     model = components
#     context_object_name = "context_list"
#     template_name = "generic_list.html"
#     add_new_url = reverse_lazy('admin:component_components_add')
#     extra_context = {
#         'title': 'Component List',
#         'add_url': add_new_url,
#         'model_name': model._meta.verbose_name
#     }


def component_list_view(request):
    component_list = components.objects.all()
    html_str = "<table><tr><th>Title</th><th>Status</th><th>controls</th></tr>"
    for comp in component_list:
        ctrl_list = []
        for ctrl in comp.implemented_controls_list():
            ctrl_list.append(ctrl.control_id)
        html_str += "<tr><td>%s<td><td>%s<td><td>%s<td>" % (comp.title, comp.status, ', '.join(ctrl_list))
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
