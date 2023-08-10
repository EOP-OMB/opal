from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from common.models import props
from component.models import components
from component.forms import ComponentForm


def component_list_view(request):
    component_list = components.objects.all()
    html_str = "<table class='table primary'><tr><th>Title</th><th>Status</th><th>Controls</th></tr>"
    for comp in component_list:
        ctrl_list = comp.list_implemented_controls()
        html_ctrl_list = []
        for ctrl in ctrl_list:
            html_ctrl_list.append("<a href='%s' target='_blank'>%s</a>" % (ctrl.get_absolute_url(), ctrl.control_id))
        html_str += "<tr><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>" % (comp.get_absolute_url(),comp.title, comp.status, ', '.join(html_ctrl_list))
    html_str += "</table><p><a href='%s'>Add new component</a></p>" % reverse_lazy('component:components_form_view')
    context = {
        'content': html_str,
        'title': 'Component List'
    }
    return render(request, "generic_template.html", context)


class component_detail_view(DetailView):
    model = components
    context_object_name = "context"
    template_name = "generic_detail.html"


def components_form_view(request):
    context = {}
    form = ComponentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        scope_prop_id, _ = props.objects.get_or_create(name='Scope',value=form.data['scope'])
        policy_owner_prop_id, _ = props.objects.get_or_create(name='Policy Owner',value=form.data['policy_owner'])
        review_interval_prop_id, _ = props.objects.get_or_create(name='Review Interval',value=form.data['review_interval'])
        new_component = form.save()
        # new_component.props.add(scope_prop_id)
        # new_component.props.add(policy_owner_prop_id)
        # new_component.props.add(review_interval_prop_id)
        new_component.save()
        return HttpResponseRedirect(reverse("component:component_detail_view", kwargs={'pk': new_component.id}))

    context['form'] = form
    return render(request, "generic_form.html", context)
