from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .models import Lids


class AddLids(CreateView):
    model = Lids
    fields = ['lid_status', 'owner', 'channel', 'interest', 'interest_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailLids(DetailView):
    model = Lids
    template_name = 'lids/detail_lid.html'


class ListLids(ListView):
    model = Lids


class UpdateLids(UpdateView):
    model = Lids
    fields = ['lid_status', 'channel', 'interest', 'interest_text']
    template_name_suffix = "_update_form"


class DeleteLids(DeleteView):
    model = Lids
    success_url = reverse_lazy("lids:list_lids")


class UpdateStatus(UpdateLids):
    fields = ['lid_status']
    template_name = 'lids/update_status.html'
