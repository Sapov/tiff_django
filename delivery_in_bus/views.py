from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Order


# Create your views here.
class ViewAllCompleteOrdersForBus(LoginRequiredMixin, ListView):
    '''Показать все ордера которые завершины и имеют статус доставка автобусом'''
    model = Order
    paginate_by = 6
    template_name = "delivery_in_bus/view_orders_for_courier.html"

    def get_queryset(self):
        return Order.objects.filter(status_id=5).filter(delivery_id=2).order_by("-id")


def render_instruction(request, order_id):
    context = {'order_id': order_id}
    return render(request, template_name='delivery_in_bus/courier_instruction.html', context=context)



