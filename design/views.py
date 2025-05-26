from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView

class DesignDetailView(DetailView):
    model = DesignOrder
    template_name = 'design/design_detail.html'

