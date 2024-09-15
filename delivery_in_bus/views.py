from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Order


# Create your views here.
class ViewAllCompleteOrders(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 6
    template_name = "delivery_in_bus/view_orders_for_courier.html"

    def get_queryset(self):
        return Order.objects.filter(status_id=5).order_by("-id")


