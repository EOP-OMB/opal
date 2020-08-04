# Create your views here.
from django.views import generic
from .models import system_control, system_security_plan, nist_control


class nist_control_list_view(generic.ListView):
    model = nist_control


class nist_control_detail_view(generic.DetailView):
    model = nist_control


class system_control_list_view(generic.ListView):
    model = system_control


class system_control_detail_view(generic.DetailView):
    model = system_control


class system_security_plan_list_view(generic.ListView):
    model = system_security_plan


class system_security_plan_detail_view(generic.DetailView):
    model = system_security_plan
