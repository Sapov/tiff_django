from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

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


class UpdateLids(UpdateView):
    model = Lids
    fields = ['lid_status', 'name', 'email', 'phone_number', 'channel', 'interest', 'interest_text']
    template_name_suffix = "_update_form"


class DeleteLids(DeleteView):
    model = Lids
    success_url = reverse_lazy("lids:list_lids")


class UpdateStatus(UpdateLids):
    fields = ['lid_status']
    template_name = 'lids/update_status.html'
