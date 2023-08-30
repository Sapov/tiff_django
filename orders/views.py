import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from account.models import Organisation
# from account.models import Organisation
from files.models import Product
from .forms import UserOrganisationForm, NewOrder, OrderForm
from .models import Order, OrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView


# from .forms import OrderForm


# from django.contrib.auth import get_user_model


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    # form_class = OrderForm
    fields = ['organisation_payer']
    login_url = 'login'


def new_order(request):
    if request.method == 'POST':
        logging.info(f'reUSERcated{request.user}')
        form = OrderForm()
        print(form)
        print(request.user)
        # if form.is_valid():
        # logging.info(form.cleaned_data)
        organisation_payer = request.POST['organisation_payer']
        logging.info(f'organisation_payer  {organisation_payer}')
        # user = request.POST['user']
        # logging.info(f'user {user} organisation_payer {organisation_payer}')
        # context =
        # organisation = Organisation.objects.get(id=organisation_payer)
        # logging.info(organisation)

        # order = Order.objects.create(Contractor=request.user)
        # logging.info(order)
    else:
        form = OrderForm()
    return render(request, 'add_new_order.html', {'form': form, })


class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['order', 'product']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def view_order(request):
    '''Вывод файлов только авторизованного пользователя'''
    Orders = Order.objects.filter(Contractor=request.user).order_by('-id')
    return render(request, "view_orders.html", {"Orders": Orders, 'title': 'Заказы'})


class View_order_item(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ("__all__")
    # fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = 'order_update_form.html'
    login_url = 'login'


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['id', 'date_complete', 'comments', 'paid']
    template_name_suffix = '_update_form'


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:view_orders')


def add_files_in_order(request, order_id):
    Orders = Order.objects.get(id=order_id)
    items = Product.objects.filter(in_order=False,
                                   Contractor=request.user)  # Только те файлы которые еще были добавлены в заказ(ы) , только файлы юзера
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
    # return render(request, "add_in.html", context)
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def del_item_in_order(request, item_id, order_id):
    Orders = Order.objects.get(id=order_id)
    old_ord = OrderItem.objects.get(id=item_id)  # строка заказа
    old_ord.delete()
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    context = {'Orders': Orders, 'items_in_order': items_in_order, 'curent_order': curent_order}
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def order_pay(request, order_id):
    Orders = Order.objects.get(id=order_id)
    curent_order = Order.objects.get(pk=order_id)
    text = 'Оплатить можно на карту 0000 0000 0000 0000'
    context = {'Orders': Orders, 'curent_order': curent_order, 'text': text}
    return render(request, "orderpay.html", context)


@login_required
def view_all_orders(request):
    '''Посмотреть все заказы '''
    Orders = Order.objects.all().order_by('id')
    return render(request, "all_view_orders.html", {"Orders": Orders, 'title': 'Заказы в работе'})


class ViewAllPayOrders(LoginRequiredMixin, ListView):
    '''Посмотреть все заказы которы оплачены и поэтому в работе'''

    model = Order
    template_name = 'all_view_orders_pay.html'

    def get_queryset(self):
        queryset = Order.objects.filter(paid=True).order_by('id')
        return queryset


def about_file(request, file_id):
    print(file_id)
    files = Product.objects.filter(id=file_id)
    print(files)
    return render(request, 'about_file.html', {'files': files})


@login_required
def view_all_files_for_work_in_orders(request):
    '''Посмотреть все файлы в заказах в статусе paid'''

    num = []
    Orders = Order.objects.filter(paid=True).order_by('id')
    for order in Orders:
        items_in_order = OrderItem.objects.filter(order=order.id)  # файлы в заказе
        num.append(items_in_order)

    return render(request, "view_all_files_for_work_in_orders.html",
                  {"Orders": Orders, 'num': num, 'title': 'Заказы в работе'})


def New_ord(request):
    form = OrderForm
    return render(request, 'neworder.html')


def user_organization_view(request):
    # if request.method == 'POST':
    user = request.user
    form = UserOrganisationForm(user=user)
    # a1 = Order.objects.create(**form.cleaned_data)
    return render(request, 'user_organization.html', {'form': form})


# def order_pay_check(request, order_id):
# Orders = Order.objects.get(id=order_id)
# # print(Orders)
# items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
# print(items_in_order)
# for i in items_in_order:
#     print('#', i.id)
#     f = Product.objects.get(id=i.id)
#     print(f.status_product.id)
#     f.status_product.id = 3
#     f.status_product.save()
#     print(f.status_product)
# text = 'Оплатить можно на карту 0000 0000 0000 0000'
# context = {'Orders': Orders, 'text': text}
# return render(request, "orderpay.html", context)


def report_complite_orders(request):
    '''Отчет от выполненных заказах'''
    #
    # date_start = request.POST['date_start']
    # date_finish = request.POST['date_finish']
    # print(date_finish, date_start)
    order = Order.objects.filter(status=3)

    return render(request, "report_complite_orders.html",
                  {"order": order, 'title': 'Заказы в работе'})
