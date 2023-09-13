import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from account.models import Organisation
# from account.models import Organisation
from files.models import Product
from .forms import NewOrder
from .models import Order, OrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView
from .utils import DrawOrder
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)


@login_required
def new_order(request):
    logging.info(request)
    if request.POST:
        logging.info(f'method POST')
        form = NewOrder(user=request.user)
        # if form.is_valid():
        logging.info(f'пришло во view {form.user}')
        logging.info(f'organisation_payer {request.POST["organisation_payer"]}')
        number_organisation = request.POST["organisation_payer"]
        organisation = Organisation.objects.get(id=number_organisation)
        logging.info(f'organisation {organisation}')
        neworder = Order.objects.create(Contractor=form.user, organisation_payer=organisation)
        logging.info(f'neworder {neworder}')
        logging.info(f'neworder {neworder.id}')
        return redirect('orders:add_file_in_order', neworder.id)
    else:
        form = NewOrder(user=request.user)
    return render(request, 'neworder.html', {'form': form})


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
    logger.info(f'Orders: {Orders}')

    paginator = Paginator(Orders, 2)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    logger.info(f'page_NUM: {page_num}')
    page_obj = paginator.get_page(page_num)
    logger.info(f'page_NUM: {page_obj}')

    return render(request, "view_orders.html", {"Orders": Orders, 'title': 'Заказы', 'page_obj': page_obj})


class OrdersViewList(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Order
    template_name = 'view_orders.html'
    login_url = 'login'


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
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def del_item_in_order(request, item_id, order_id):
    Orders = Order.objects.get(id=order_id)
    old_ord = OrderItem.objects.get(id=item_id)  # строка заказа
    old_ord.delete()
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    context = {'Orders': Orders, 'items_in_order': items_in_order, 'curent_order': curent_order}
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def goto_folder_orders(foo):
    ''' переходим в папку media/orders  и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
        curent_path = os.getcwd()
        # logger.info(f'[INFO DECORATOR] OBJECT: {order_id}')
        # data_file = Product.objects.get(id=self.order_id)
        # logger.info(f'[INFO DECORATOR] OBJECT: {data_file}')
        # logger.info(f'[INFO DECORATOR] CREATED: {data_filea_file.created}')
        # перейти в директорию дата должна браться из параметра Order.created
        os.chdir(
            f'{settings.MEDIA_ROOT}/orders')
        logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
        res = foo(*args, **kwargs)
        os.chdir(curent_path)  # перейти обратно
        logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
        return res

    return wrapper


@goto_folder_orders
def order_pay(request, order_id):
    Orders = Order.objects.get(id=order_id)
    curent_order = Order.objects.get(pk=order_id)
    text = 'Оплатить можно на карту 0000 0000 0000 0000'
    # --------------- order pdf----------
    logging.info(curent_order.organisation_payer, curent_order.organisation_payer.inn)
    order_pdf = DrawOrder(order_id)
    order_pdf.run()
    context = {'Orders': Orders, 'curent_order': curent_order, 'text': text}
    return render(request, "orderpay.html", context)


# @login_required
# def view_all_orders(request):
#     '''Посмотреть все заказы'''
#     object_list = Order.objects.all().order_by('-id')
#
#     paginator = Paginator(Orders, 2)
#     if 'page' in request.GET:
#         page_num = request.GET.get('page')
#     else:
#         page_num = 1
#     logger.info(f'page_NUM: {page_num}')
#     page_obj = paginator.get_page(page_num)
#     logger.info(f'page_NUM: {page_obj}')
#
#     return render(request, "all_view_orders.html",
#                   {"object_list": object_list, 'title': 'Заказы в работе', 'page_obj': page_obj})


class AllOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "all_view_orders.html"
    paginate_by = 6

    def get_queryset(self):
        ''' для обратного порядка отображения'''
        queryset = Order.objects.all().order_by('-id')
        return queryset


class ViewAllPayOrders(LoginRequiredMixin, ListView):
    '''Посмотреть все заказы которые оплачены и поэтому в работе'''

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
    Orders = Order.objects.filter(paid=True).order_by('-id')
    for order in Orders:
        items_in_order = OrderItem.objects.filter(order=order.id)  # файлы в заказе
        num.append(items_in_order)

    return render(request, "view_all_files_for_work_in_orders.html",
                  {"Orders": Orders, 'num': num, 'title': 'Заказы в работе'})


def user_organization_view(request):
    # if request.method == 'POST':
    user = request.user
    form = UserOrganisationForm(user=user)
    # a1 = Order.objects.create(**form.cleaned_data)
    return render(request, 'user_organization.html', {'form': form})


def report_complite_orders(request):
    '''Отчет от выполненных заказах'''

    date_start = request.POST['date_start']
    date_finish = request.POST['date_finish']
    # logger.info(f'date_start:{date_start}')
    # logger.info(f'date_finish:{date_finish}')
    order = Order.objects.filter(status=3)

    return render(request, "report_complite_orders.html",
                  {"order": order,})


