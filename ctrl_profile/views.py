from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from ctrl_profile.models import *


# Create your views here.

class profile_list_view(ListView):
    model = profiles
    context_object_name = "context_list"
    template_name = "generic_list.html"


class profile_detail_view(DetailView):
    model = profiles
    context_object_name = "context"
    template_name = "generic_detail.html"


class createProfileView(CreateView):
    model = profiles
    fields = ['metadata', 'imports', 'merge', 'modify', 'back_matter']
