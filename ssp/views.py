from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from ssp.models import *


# Create your views here.

class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "context_list"
    template_name = "generic_list.html"


class ssp_detail_view(DetailView):
    model = system_security_plans
    context_object_name = "context"
    template_name = "generic_detail.html"
