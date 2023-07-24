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
    login_url = 'login'

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['order', 'product']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def view_order(request):
    '''Вывод файлов толоко авторизованного пользователя'''
    Orders = Order.objects.filter(Contractor=request.user).order_by('id')
    return render(request, "view_orders.html", {"Orders": Orders, 'title': 'Заказы'})


class View_order_item(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ("__all__")
    # fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = 'order_update_form.html'
    login_url = 'login'


# def all_files_in_order(request, order_id):
#     Orders = Order.objects.filter(id=order_id)
#     items = OrderItem.objects.filter(order=order_id)
#     curent_order = Order.objects.get(pk=order_id)
#     context = {'Orders': Orders, 'items': items, 'curent_order': curent_order}
#     return render(request, "all_files_in_order.html", context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['id', 'date_complete', 'comments']
    template_name_suffix = '_update_form'


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:view_orders')


def add_files_in_order(request, order_id):
    Orders = Order.objects.filter(id=order_id)
    Orders = Order.objects.get(id=order_id)
    items = Product.objects.filter(in_order=False)  # Только те файлы которые еще были добавлены в заказ(ы)
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    print('ORDER TYPE___', type(Orders))

    context = {'Orders': Orders, 'items': items, 'items_in_order': items_in_order, 'curent_order': curent_order,
               'order_id': order_id}
    return render(request, "add_files_in_order.html", context)


def add_item_in_order(request, item_id, order_id):
    Orders = Order.objects.get(id=order_id)
    new_ord = OrderItem()
    new_ord.order = Orders

    item = Product.objects.get(id=item_id)
    new_ord.product = item
    new_ord.save()
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    print('ORDER TYPE', type(Orders))
    context = {'Orders': Orders, 'items_in_order': items_in_order, 'curent_order': curent_order}
    return render(request, "add_in.html", context)
    # return render(request, "add_files_in_order.html", context)


def del_item_in_order(request, item_id, order_id):
    Orders = Order.objects.get(id=order_id)
    old_ord = OrderItem.objects.get(id=item_id)  # строка заказа
    old_ord.delete()

    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    context = {'Orders': Orders, 'items_in_order': items_in_order, 'curent_order': curent_order}
    # return render(request, "add_in.html", context)
    return render(request, "add_files_in_order.html", context)


def order_pay(request, order_id):
    Orders = Order.objects.get(id=order_id)
    curent_order = Order.objects.get(pk=order_id)
    text = 'Оплать можно на карту 0000 0000 0000 0000'
    context = {'Orders': Orders, 'curent_order': curent_order, 'text': text}
    return render(request, "orderpay.html", context)

    #
