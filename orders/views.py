from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .models import Order, OrderItem
from django.views.generic.edit import CreateView, UpdateView


class OrderCreateView(CreateView):
    model = Order
    fields = ['id', 'total_price', 'organisation_payer', 'paid', 'status']


class OrderItemCreateView(CreateView):
    model = OrderItem
    fields = ['order', 'product', 'price_per_item', 'quantity', 'total_price']

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def view_order(request):
    '''Вывод файлов толоко авторизованного пользователя'''
    Orders = Order.objects.filter(Contractor=request.user)

    return render(request, "view_orders.html", {"Orders": Orders, 'title': 'Заказы'})


# def view_order_item(request):
#     '''Вывод файлов толоко авторизованного пользователя'''
#     Orders_item = Order.objects.filter(id=id)
#     print(Orders_item)
#
#     return render(request, "view_orders_item.html", {"Orders_item": Orders_item, 'title': 'Заказы'})
class View_order_item(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ("__all__")
    # fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = 'order_update_form.html'
    login_url = 'login'


der(request, "index.html", {"product": product, 'title': 'Загрузка файлов'})