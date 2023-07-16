from django.shortcuts import render
from .models import Order
from django.views.generic.edit import CreateView


class AuthorCreateView(CreateView):
    model = Order
    fields = ['id', 'total_price', 'organisation_payer', 'paid', 'status']