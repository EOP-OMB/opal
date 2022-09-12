from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from component.models import components


class component_list_view(ListView):
    model = components
    context_object_name = "context_list"
    template_name = "generic_list.html"
    add_new_url = reverse_lazy('admin:component_components_add')
    extra_context = {
        'title': 'Component List',
        'add_url': add_new_url,
        'model_name': model._meta.verbose_name
        }


class component_detail_view(DetailView):
    model = components
    context_object_name = "context"
    template_name = "generic_detail.html"
