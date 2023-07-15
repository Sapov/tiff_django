from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView
from . models import *


# Create your views here.
class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['order', 'product', 'total_price', 'is_active']

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)