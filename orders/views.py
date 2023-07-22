from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from files.models import Product
from .models import Order, OrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['organisation_payer']


class OrderItemCreateView(CreateView):
    model = OrderItem
    fields = ['order', 'product']

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def view_order(request):
    '''Вывод файлов толоко авторизованного пользователя'''
    Orders = Order.objects.filter(Contractor=request.user)
    product = Product.objects.filter(Contractor=request.user)

    return render(request, "view_orders.html", {"Orders": Orders, 'product': product, 'title': 'Заказы'})


# def view_order_item(request):
#     '''Вывод файлов толоко авторизованного пользователя'''
#     Orders_item = Order.objects.filter(id=id)
#     print(Orders_item)
#
#     return render(request, "view_orders_item.html", {"Orders_item": Orders_item, 'title': 'Заказы'})
class View_order_item(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ("__all__")
    # fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = 'order_update_form.html'
    login_url = 'login'


def all_files_in_order(request, order_id):
    Orders = Order.objects.filter(id=order_id)
    items = OrderItem.objects.filter(order=order_id)
    curent_order = Order.objects.get(pk=order_id)
    context = {'Orders': Orders, 'items': items, 'curent_order': curent_order}
    return render(request, "all_files_in_order.html", context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['id', 'date_complete', 'comments']
    template_name_suffix = '_update_form'


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:view_order')


def add_files_in_order(request, order_id):
    Orders = Order.objects.filter(id=order_id)
    items = Product.objects.filter(in_order=False)  # Только те файлы которые еще были добавлены в заказ(ы)

    print(request)
    print(request.__dict__)
    print('ITEMS', items)
    for i in items:
        print(i.id)

    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе

    curent_order = Order.objects.get(pk=order_id)
    context = {'Orders': Orders, 'items': items, 'items_in_order': items_in_order, 'curent_order': curent_order}

    return render(request, "add_files_in_order.html", context)

#
# def addin(request, product_id):
#     product = Product.objects.get(id=product_id)
#     OrderItem.objects.create(order=product_id, product=product, price_per_item=0, quantity=0, total_price=0, )
#     items = Product.objects.filter(in_order=False)  # Только те файлы которые еще были добавлены в заказ(ы)
#     items_in_order = OrderItem.objects.filter(order=product_id)  # файлы в заказе
#     curent_order = Order.objects.get(pk=order_id)
#
#     context = {'product': product, 'items': items, 'items_in_order': items_in_order, 'curent_order': curent_order}
#
#     return render(request, "add_in.html", context)

@login_required
def order_pay(request, order_id):
    '''Pay'''
    Orders = Order.objects.filter(id=order_id)
    text = ' Оплатить можно на карту № 0000 0000 0000 0000'

    context = {'Orders': Orders, 'text':text}
    return render(request, "orderpay.html", context)
