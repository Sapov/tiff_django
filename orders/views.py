from django.shortcuts import render
from .forms import *


# Create your views here.
def add_order(request):
    form = FormsOrderItem()
    return render(request, "add_order.html", {"form": form, 'title': 'order'})
