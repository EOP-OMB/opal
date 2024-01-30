from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView

from common.models import props
from component.models import components
from component.forms import ComponentForm

GENERIC_FORM_HTML = "generic_form.html"

COMPONENT_DETAIL_VIEW = "component:component_detail_view"


def component_list_view(request):
    component_list = components.objects.all()
    html_str = "<table class='table primary'><tr><th>Title</th><th>Status</th><th>Controls</th></tr>"
    for comp in component_list:
        ctrl_list = comp.list_implemented_controls()
        html_ctrl_list = []
        for ctrl in ctrl_list:
            html_ctrl_list.append("<a href='%s' target='_blank'>%s</a>" % (ctrl.get_absolute_url(), ctrl.control_id))
        html_str += "<tr><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>" % (comp.get_absolute_url(), comp.title, comp.status, ', '.join(html_ctrl_list))
    html_str += "</table><p>"
    context = {
        'content': html_str,
        'title': 'Component List'
    }
    return render(request, "generic_template.html", context)


class component_detail_view(DetailView):
    model = components
    context_object_name = "context"
    template_name = "generic_detail.html"


def component_form_view(request):
    context = {}
    form = ComponentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_component = form.save()
        return redirect(reverse(COMPONENT_DETAIL_VIEW, kwargs={'pk': new_component.id}))

    context['form'] = form
    return render(request, GENERIC_FORM_HTML, context)


def policy_component_form_view(request):
    context = {}
    form = ComponentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        scope_prop_id, _ = props.objects.get_or_create(name='Scope', value=form.data['scope'])
        policy_owner_prop_id, _ = props.objects.get_or_create(name='Policy Owner', value=form.data['policy_owner'])
        review_interval_prop_id, _ = props.objects.get_or_create(name='Review Interval', value=form.data['review_interval'])
        new_component = form.save()
        new_component.props.add(scope_prop_id)
        new_component.props.add(policy_owner_prop_id)
        new_component.props.add(review_interval_prop_id)
        new_component.save()
        return redirect(reverse(COMPONENT_DETAIL_VIEW, kwargs={'pk': new_component.id}))

    form.fields['type'] = forms.CharField(widget=forms.HiddenInput(), initial="policy")
    form.fields['scope'] = forms.CharField(max_length=100)
    form.fields['review_interval'] = forms.CharField(max_length=100)
    user_name_display = "%s %s <%s>" % (request.user.first_name, request.user.last_name, request.user.email)
    form.fields['policy_owner'] = forms.CharField(initial=user_name_display, max_length=1000)

    form.field_order = ['type', 'title', 'purpose', 'status', 'scope', 'policy_owner', 'review_interval', 'description']

    context['form'] = form
    context['title'] = 'Add New Policy'
    return render(request, GENERIC_FORM_HTML, context)


def cloud_service_component_form_view(request):
    context = {}
    form = ComponentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        url_prop_id, _ = props.objects.get_or_create(name='URL', value=form.data['url'])
        application_owner_prop_id, _ = props.objects.get_or_create(name='Application Owner', value=form.data['application_owner'])
        new_component = form.save()
        new_component.props.add(url_prop_id)
        new_component.props.add(application_owner_prop_id)
        new_component.save()
        return redirect(reverse(COMPONENT_DETAIL_VIEW, kwargs={'pk': new_component.id}))

    form.fields['type'] = forms.CharField(widget=forms.HiddenInput(), initial="service")
    form.fields['title'] = forms.CharField(max_length=1000, label="Name", widget=forms.TextInput(attrs={'size': "100"}))
    form.fields['url'] = forms.URLField(max_length=1000, label="URL", widget=forms.TextInput(attrs={'size': "100"}))
    form.fields['application_owner'] = forms.CharField(initial=request.user, max_length=100)

    form.order_fields(['type', 'title', 'purpose', 'status', 'url', 'application_owner', 'description'])

    context['form'] = form
    context['title'] = 'Add New Cloud Service'
    return render(request, "generic_form.html", context)


def social_media_component_form_view(request):
    context = {}
    form = ComponentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        url_prop_id, _ = props.objects.get_or_create(name='URL', value=form.data['url'])
        application_owner_prop_id, _ = props.objects.get_or_create(name='Application Owner', value=form.data['application_owner'])

        account_id, _ = props.objects.get_or_create(name='account_id', value=form.data['account_id'])
        approval_process, _ = props.objects.get_or_create(name='approval_process', value=form.data['approval_process'])
        new_component = form.save()
        new_component.props.add(url_prop_id)
        new_component.props.add(application_owner_prop_id)
        new_component.props.add(account_id)
        new_component.props.add(approval_process)
        new_component.save()
        return redirect(reverse('component:component_list_view'))

    form.fields['type'] = forms.CharField(widget=forms.HiddenInput(), initial="social_media")
    form.fields['title'] = forms.CharField(max_length=1000, label="Name", widget=forms.TextInput(attrs={'size': "100"}))
    form.fields['url'] = forms.URLField(max_length=1000, label="URL", widget=forms.TextInput(attrs={'size': "100"}))
    form.fields['account_id'] = forms.CharField(max_length=1000, label="Social Media Account ID", widget=forms.TextInput(attrs={'size': "100"}))
    form.fields['application_owner'] = forms.CharField(initial=request.user, max_length=100)
    form.fields['approval_process'] = forms.CharField(widget=forms.TextInput(), label="How are postings approved?")

    form.order_fields(['type', 'title', 'purpose', 'status', 'url', 'application_owner', 'description', 'approval_process'])

    context['form'] = form
    context['title'] = 'Add New Social Media Account/Service'
    return render(request, "generic_form.html", context)
