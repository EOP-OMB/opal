from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from ctrl_profile.models import ctrl_profiles


# Create your views here.

class profile_list_view(ListView):
    model = ctrl_profiles
    context_object_name = "context_list"
    template_name = "generic_list.html"


class profile_detail_view(DetailView):
    model = ctrl_profiles
    context_object_name = "context"
    template_name = "generic_detail.html"


class createProfileView(CreateView):
    model = ctrl_profiles
    fields = ['metadata', 'imports', 'merge', 'modify', 'back_matter']
    template_name = "generic_form.html"
