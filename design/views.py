from django.shortcuts import render
from django.views.generic import ListView

from design.models import OrderDesign


# Create your views here.
class DesignViewList(ListView):
    model = OrderDesign
    template_name = 'design_list.html'