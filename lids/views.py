from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from .models import Lids


# Create your views here.

class AddLids(CreateView):
    model = Lids
    fields = ['lid_status', 'name', 'email', 'phone_number', 'channel', 'interest', 'interest_text']


class DetailLids(DetailView):
    model = Lids
    template_name = 'lids/detail_lid.html'


class ListLids(ListView):
    model = Lids
