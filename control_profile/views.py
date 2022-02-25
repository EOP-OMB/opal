from django.shortcuts import render
from django.views.generic.edit import CreateView
from control_profile.models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.

class profile_list_view(ListView):
    model = profile
    context_object_name = "profile_list"


class profile_detail_view(DetailView):
    model = profile
    context_object_name = "profile"
    template_name = "profile/profile_detail.html"

class createProfileView(CreateView):
    model = profile
    fields = ['metadata','imports','merge','modify','back_matter']

