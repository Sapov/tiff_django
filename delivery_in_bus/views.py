from django.shortcuts import render

from orders.models import Order
from orders.views import ViewAllPayOrders


# Create your views here.
class ViewAllCompleteOrders(ViewAllPayOrders):
    template_name = "view_orders_for_courier.html"

    def get_queryset(self):
        return Order.objects.filter(status_id=5).order_by("-id")