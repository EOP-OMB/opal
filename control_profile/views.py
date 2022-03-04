from django.shortcuts import render
from django.views.generic.edit import CreateView
from control_profile.models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.

class profile_list_view(ListView):
    model = profile
    context_object_name = "context_list"
    template_name = "generic_list.html"


class profile_detail_view(DetailView):
    model = profile
    context_object_name = "context"
    template_name = "generic_detail.html"

class createProfileView(CreateView):
    model = profile
    fields = ['metadata','imports','merge','modify','back_matter']

