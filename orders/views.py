import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from account.models import Organisation, Delivery

# from account.models import Organisation
from files.models import Product
from files.pay import Robokassa
from .forms import NewOrder
from .models import Order, OrderItem, UtilsModel
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView
from .utils import DrawOrder, Utils
from django.core.paginator import Paginator
from .tasks import arh_for_mail
import logging

logger = logging.getLogger(__name__)


@login_required
def new_order(request):
    logging.info(request)
    if request.POST:
        logging.info(f"method POST")
        # form = NewOrder(user=request.user)  # для организаций пока отключу
        form = NewOrder()  # для организаций пока отключу
        # if form.is_valid():
        # logging.info(f"USER: {form.user}")
        # logging.info(f'ORGANISATION: {request.POST["organisation_payer"]}')
        logging.info(f'delivery {request.POST["delivery"]}')
        logging.info(f'REQUEST {request.POST}')
        logging.info(f'USER {request.user}')
        # если агентство добавляем оранизацию платильщик
        # number_organisation = request.POST["organisation_payer"]
        # organisation = Organisation.objects.get(id=number_organisation)
        # logging.info(f"organisation {organisation}")
        delivery_id = request.POST["delivery"]

        delivery = Delivery.objects.get(id=delivery_id)

        # neworder = Order.objects.create(
        #     Contractor=form.user, organisation_payer=organisation, delivery=delivery,
        # )

        neworder = Order.objects.create(Contractor=request.user, delivery=delivery)

        # logging.info(f"neworder {neworder}")
        # logging.info(f"NEW ORDER ID: {neworder.id}")
        return redirect("orders:add_file_in_order", neworder.id)
    else:
        form = NewOrder()
    return render(request, "neworder.html", {"form": form})


@login_required
def view_order(request):
    """Вывод файлов только авторизованного пользователя"""
    Orders = Order.objects.filter(Contractor=request.user).order_by("-id")
    logger.info(f"Orders:  {Orders}")

    paginator = Paginator(Orders, 2)
    if "page" in request.GET:
        page_num = request.GET.get("page")
    else:
        page_num = 1
    logger.info(f"page_NUM: {page_num}")
    page_obj = paginator.get_page(page_num)
    logger.info(f"page_NUM: {page_obj}")

    return render(
        request,
        "view_orders.html",
        {"Orders": Orders, "title": "Заказы", "page_obj": page_obj},
    )


class OrdersViewList(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Order
    template_name = "view_orders.html"
    login_url = "login"


class View_order_item(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = "__all__"
    # fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = "order_update_form.html"
    login_url = "login"


class OrderUpdateView(UpdateView):
    model = Order
    fields = ["id", "date_complete", "comments", "paid"]
    template_name_suffix = "_update_form"


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy("orders:view_orders")


def add_files_in_order(request, order_id):
    Orders = Order.objects.get(id=order_id)
    items = Product.objects.filter(
        in_order=False, Contractor=request.user
    )  # Только те файлы которые еще были добавлены в заказ(ы) , только файлы юзера
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    current_order = Order.objects.get(pk=order_id)

    context = {
        "Orders": Orders,
        "items": items,
        "items_in_order": items_in_order,
        "current_order": current_order,
        "order_id": order_id,
    }
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
    context = {
        "Orders": Orders,
        "items_in_order": items_in_order,
        "curent_order": curent_order,
    }
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def del_item_in_order(request, item_id, order_id):
    Orders = Order.objects.get(id=order_id)
    old_ord = OrderItem.objects.get(id=item_id)  # строка заказа
    old_ord.delete()
    old_ord.save()

    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    context = {
        "Orders": Orders,
        "items_in_order": items_in_order,
        "curent_order": curent_order,
    }
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def order_pay(request, order_id):
    """ОФОРМИТЬ ЗАКАЗ - Меняем статус с загружен на оформлен
    генерируем счет
    """
    current_path = os.getcwd()
    os.chdir(f"{settings.MEDIA_ROOT}/orders")
    text = 'оплата text'

    # --------------- Формирование счета---------
    # create_order_pdf.delay(order_id)
    # order_pdf = DrawOrder(order_id)  #
    # order_pdf.run()

    # _________________________Архивируем файлы для письма посылаем письмо с заказом------------------
    domain = str(get_domain(request))
    arh_for_mail.delay(order_id, domain=domain)

    # -----------------------create_link_pay-----------------------------------
    Orders = Order.objects.get(id=order_id)
    user = request.user
    link_pay = Robokassa(Orders.total_price, f'Оплата заказа № {Orders.id}', order_id, user).run()
    # logger.info(f'Генерим платежную ссылку: ', link_pay)
    context = {"Orders": Orders, "text": text, 'link_pay': link_pay}
    os.chdir(current_path)  # перейти обратно

    return render(request, "orderpay.html", context)


def get_domain(request):
    logger.info(f"DOMAIN: {get_current_site(request)}")
    return str(get_current_site(request))


class AllOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "all_view_orders.html"
    paginate_by = 6

    def get_queryset(self):
        """для обратного порядка отображения"""
        queryset = Order.objects.all().order_by("-id")
        return queryset


class ViewAllPayOrders(LoginRequiredMixin, ListView):
    """Посмотреть все заказы которые оплачены и поэтому в работе"""

    model = Order
    template_name = "all_view_orders_pay.html"

    def get_queryset(self):
        queryset = Order.objects.filter(paid=True).order_by("id")
        return queryset


def about_file(request, file_id):
    print(file_id)
    files = Product.objects.filter(id=file_id)
    print(files)
    return render(request, "about_file.html", {"files": files})


@login_required
def view_all_files_for_work_in_orders(request):
    """Посмотреть все файлы в заказах в статусе paid"""

    num = []
    Orders = Order.objects.filter(paid=True).order_by("-id")
    for order in Orders:
        items_in_order = OrderItem.objects.filter(order=order.id)  # файлы в заказе
        num.append(items_in_order)

    return render(
        request,
        "view_all_files_for_work_in_orders.html",
        {"Orders": Orders, "num": num, "title": "Заказы в работе"},
    )


# def user_organization_view(request):
#     # if request.method == 'POST':
#     user = request.user
#     form = UserOrganisationForm(user=user)
#     # a1 = Order.objects.create(**form.cleaned_data)
#     return render(request, "user_organization.html", {"form": form})


def report_complite_orders(request):
    """Отчет от выполненных заказах"""

    if request.method == "POST":
        date_start = request.POST["date_start"]
        date_finish = request.POST["date_finish"]
        logger.info(f"date_start:{date_start}, type{type(date_start)}")
        logger.info(f"date_finish:{date_finish}")
        order = Order.objects.filter(created=2023-10-10)
        return render(request, "report_complite_orders.html", {"order": order})



    else:
        # form = Calculator()
        return render(request, "report_complite_orders.html")


def result(request):
    if request.GET:
        if 'OutSum' and 'InvId' in request.GET:
            received_sum = request.GET['OutSum']
            order_number = request.GET['InvId']
            received_signature = request.GET['SignatureValue']

            if Robokassa.check_signature_result(received_sum, order_number, received_signature,
                                                os.getenv('PASSWORD_ONE'), ):
                # переключаем оплату на TRUE
                return render(request, 'success_pay.html')

            # http://www.orders.san-cd.ru/success/?OutSum=12.00&InvId=1&SignatureValue=356f165b0869ab28c62c6c063c44bccb&IsTest=1&Culture=ru
        return render(request, 'fail_pay.html')


def success_pay(request):
    if request.GET:
        print(request.GET)

        received_sum = request.GET['OutSum']
        order_number = request.GET['InvId']
        received_signature = request.GET['SignatureValue']

        if Robokassa.check_signature_result(received_sum, order_number, received_signature,
                                            os.getenv('PASSWORD_ONE'), ):
            return render(request, 'success_pay.html')
    return render(request, 'fail_pay.html')


def fail(request):
    return render(request, 'fail_pay.html')
