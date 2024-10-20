import os
from datetime import date, datetime
import datetime
import json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django_celery_beat.models import PeriodicTask

from account.models import Delivery, Organisation

from files.models import Product, StatusProduct
from files.pay import Robokassa
from .alerts import Alerts
from .forms import NewOrder, ReportForm
from .models import Order, OrderItem, StatusOrder
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView
from django.core.paginator import Paginator

from .payment.bank import Bank
from .tasks import arh_for_mail, create_order_pdf, send_message_whatsapp
import logging
import jwt
from jwt import exceptions
from jwt import jwk_from_dict

import json

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

User = get_user_model()

logger = logging.getLogger(__name__)


@login_required
def new_order(request):
    logging.info(request)
    if request.POST:
        logging.info(f"method POST")
        form = NewOrder(user=request.user)
        # if form.is_valid():
        # logging.info(f'delivery_address {request.POST["delivery_address"]}')
        logging.info(f"REQUEST {request.POST}")
        logging.info(f"USER {request.user}")
        date_complite = request.POST["date_complite"]
        logging.info(f'[INFO] отправленная форма имеет дату {date_complite}')
        date_complite = datetime.datetime.strptime(date_complite, "%Y-%m-%d")
        logging.info(f'[INFO] Приводим строку в формату даты {date_complite}')
        date_complite += datetime.timedelta(hours=12)  # чтоб отдавать в 12 часов
        logging.info(f'[INFO] прибавляем 12 часов {date_complite}')

        logging.info(f"date_complite {date_complite} - {type(date_complite)}")
        delivery_id = request.POST["delivery"]
        logging.info(f"DELIV ID:  {delivery_id}")
        logging.info(f"ORGANISATION:  {request.POST['organisation_payer']}")

        delivery = Delivery.objects.get(id=delivery_id)
        logging.info(f"DELIVERY:  {delivery}")
        organisation_id = request.POST['organisation_payer']
        if organisation_id:
            organisation = Organisation.objects.get(id=organisation_id)
        else:
            organisation = None

        neworder = Order.objects.create(
            Contractor=form.user,
            date_complete=date_complite,
            organisation_payer=organisation,
            delivery=delivery,
        )

        return redirect("orders:add_file_in_order", neworder.id)
    else:
        form = NewOrder(user=request.user)
        # ограничение по дням нельзя сделать заказ раньше сегодняшней даты
        today = select_time_complete(datetime.datetime.today())
    return render(request, "neworder.html", {"form": form, "today": today})


def select_time_complete(today: datetime) -> str:
    ''' Выбор времени готовности заказа'''
    logging.info(f"[ДАТА ГОТОВНОСТИ + ДВА ДНЯ К ДАТЕ ЗАКАЗА] {today.isoweekday()}")
    # Если заказ приняли в четверг, то отдадим только в понедельник
    if today.isoweekday() == 4:
        # + 4 дня так как два выходных
        today = today + datetime.timedelta(days=4)
        # Оформленный в пятницу будет готов в понедельник
    elif today.isoweekday() == 5 or today.isoweekday() == 6:
        today = today + datetime.timedelta(days=3)
    # Оформленный заказ в субботу готов будет во вторник + 3
    # Оформленный заказ в воскресенье готов во вторник + 2
    else:
        today = today + datetime.timedelta(days=2)
    today = today.strftime("%Y-%m-%d")
    return today


@login_required
def view_order(request):
    """Вывод Заказов только авторизованного пользователя"""
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
        Contractor=request.user
    )  # Только те файлы которые еще были добавлены в заказ(ы), только файлы юзера
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

    set_status_file(item, 2)
    items_in_order = OrderItem.objects.filter(order=order_id)  # файлы в заказе
    curent_order = Order.objects.get(pk=order_id)
    context = {
        "Orders": Orders,
        "items_in_order": items_in_order,
        "curent_order": curent_order,
    }
    return redirect(f"/orders/add_files_in_order/{order_id}")  # редирект на заказ


def set_status_file(item, status_id: int):
    instance_status = StatusProduct.objects.get(id=status_id)  # файл в работе
    item.status_product = instance_status
    item.save()


def del_item_in_order(request, order_id: int, item_id: int, item_product_id: int):
    '''Удаляет файл из заказа, но оставляет его в списке файлов'''
    Orders = Order.objects.get(id=order_id)
    old_item = OrderItem.objects.get(id=item_id)  # строка заказа
    old_item.delete()

    item = Product.objects.get(id=item_product_id)
    set_status_file(item, 1)  # файл в загружен
    logging.info(f'[Удаляем из OrderItems] {old_item}')

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
    order = Order.objects.get(id=order_id)

    if str(order.status) != 'Оформлен':  # предотвращаем повторную отправку заказа

        # _________________________Архивируем файлы для письма посылаем письмо с заказом------------------
        domain = str(get_domain(request))
        arh_for_mail.delay(order_id, domain=domain)

        # ----------''' Сообщение администратору'''--------------
        ''' В будущем - -Сообщение менеджеру типографии'''
        admin_phone = os.getenv('PHONE_NUMBER')
        send_message_whatsapp.delay(f'{admin_phone}', f'Письмо отправлено в типографию. '
                                                      f'Заказ № {order_id} оформлен')

        # ------------Устанавливаем таймер на готовность заказа по истечении таймера отправляем письмо с вопросом о готовности----------------
        # получаем дату готовности из базы

        Alerts.start_count_down(domain, order_id)
        # -----------------------create_link_pay-----------------------------------
        Orders = Order.objects.get(id=order_id)
        user = request.user
        link_pay = Robokassa(Orders.total_price, f'Оплата заказа № {Orders.id}', order_id, user).run()
        # logger.info(f'Генерим платежную ссылку: ', link_pay)
        context = {"Orders": Orders, 'link_pay': link_pay}
        # ________ГЕНЕРИМ СЧЕТ ОТ ТОЧКИ ПО API______________
        # только если была выбрана организация
        if Orders.organisation_payer:
            print('Генерим счет')
            create_order_pdf.delay(order_id)
        # оповещаем в whatsapp
        item_user = User.objects.get(email=user)
        if item_user.whatsapp and item_user.phone_number:
            send_message_whatsapp.delay(f'7{item_user.phone_number.national_number}', f'Заказ № {order_id} оформлен')

        os.chdir(current_path)  # перейти обратно

        return render(request, "orderpay.html", context)
    else:
        return render(request, "orderpay.html")


def stop_count_down(order_id: int):
    '''Останавливаем отсылку писем с вопросами о готовности заказа'''
    try:
        item_periodic_task = PeriodicTask.objects.get(name=f'Timer count Down order №{order_id}')
        item_periodic_task.enabled = False
        item_periodic_task.save()
        item_periodic_task.delete()
    except Exception as Ex:
        print('Нет уже задачи', Ex)


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
    paginate_by = 6

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


def report_complete_orders(request):
    """Отчет оп выполненным заказам"""

    if request.method == "POST":
        form = ReportForm(request.POST)
        date_start = request.POST["date_start"]
        date_finish = request.POST["date_finish"]
        logger.info(f"date_start:{date_start}, type{type(date_start)}--{date_start}")
        logger.info(f"date_finish:{date_finish}")

        if form.is_valid():
            # проверяем что выбрали дату и строка пришла не пустая
            if len(date_start) == 0 or len(date_finish) == 0:
                form = ReportForm()
                return render(request, "report_complite_orders.html", {'form': form})

            '''
            events_within_date_range = Event.objects.filter(
    event_date__gte=datetime.combine(date(2023, 3, 14), datetime.min.time()),
    event_date__lt=datetime.combine(date(2023, 3, 15), datetime.min.time())
)
Приведенный выше запрос вернет события, происходящие с 14 марта и до, но не включающего, 15 марта 2023 года. 
Создание комбинированной даты и времени через datetime.combine с использованием datetime.min.time() в примере выше 
включает все моменты времени данного дня.
            '''
            order = Order.objects.filter(
                created__gte=datetime.datetime.combine(date(int(date_start[:4]), int(date_start[5:7]),
                                                            int(date_start[8:])),
                                                       datetime.datetime.min.time()),
                created__lt=datetime.datetime.combine(date(int(date_finish[:4]), int(date_finish[5:7]),
                                                           int(date_finish[8:])),
                                                      datetime.datetime.min.time()))
            logger.info(f'ОРДЕРА: {order}')
            all_total_price = all_cost_total_price = 0
            for i in order:
                if i.total_price != None or i.cost_total_price != None:
                    all_total_price += i.total_price
                    all_cost_total_price += i.cost_total_price
            context_dic = {form: 'form',
                           "order": order,
                           'all_total_price': all_total_price,
                           'all_cost_total_price': all_cost_total_price,
                           'date_start': date_start,
                           'date_finish': date_finish}

            return render(request, "report_complite_orders.html", context=context_dic)


    else:
        form = ReportForm()
        return render(request, "report_complite_orders.html", {'form': form})


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


def report_day(request):
    ''' ОТчет о заказах за день'''
    date_now = datetime.datetime.now()
    order = Order.objects.filter(created__date=date(date_now.year, date_now.month, date_now.day))

    all_total_price = all_cost_total_price = 0
    for i in order:
        if i.total_price is not None or i.cost_total_price is not None:
            all_total_price += i.total_price
            all_cost_total_price += i.cost_total_price
            context = {
                "order": order,
                'all_total_price': all_total_price,
                'all_cost_total_price': all_cost_total_price,
            }

    return render(request, "orders/report_day.html", context=context)


def change_status_order(status_oder: int, pk: int):
    order = Order.objects.get(id=pk)  # получаем заказ по id заказа
    status = StatusOrder.objects.get(id=status_oder)  # меняем статус заказа
    logger.info(f"МЕНЯЮ СТАТУС НА {status}")
    order.status = status
    order.save()


def create_invoice(request, order_id):
    domain = str(get_domain(request))
    # order = Bank(order_id)
    # order.run()
    item = Order.objects.get(id=order_id)
    context = {'title': 'Счет на оплату услуг', 'link_pdf': f"http://{domain}/media/{str(item.order_pdf_file)}"}
    return render(request, 'orders/create_invoice.html', context)


@csrf_exempt
@require_POST
@non_atomic_requests
def web_hook(request):
    if request.method == 'POST':
        # Публичный ключ Точки. Может быть получен из https://enter.tochka.com/doc/openapi/static/keys/public
        public_key_bank = os.getenv('PUBLIC_KEY_BANK')
        payload = request.body
        st = payload.decode('utf-8')
        key_json = public_key_bank
        key = json.loads(key_json)
        jwk_key = jwt.jwk_from_dict(key)
        try:
            # тело вебхука
            webhook_jwt = jwt.JWT().decode(
                message=st,
                key=jwk_key,
            )
            json_hook = json.dumps(webhook_jwt, indent=4, ensure_ascii=False)
            print(json_hook)
            admin_phone = os.getenv('PHONE_NUMBER')
            send_message_whatsapp.delay(f'{admin_phone}', f'Пришло оповещение о оплате: {json_hook}')


        except exceptions.JWTDecodeError:
            # Неверная подпись, вебхук не от Точки или с ним что-то не так
            pass

        return HttpResponse(status=200)
