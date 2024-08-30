import json
import logging
import os
from datetime import date, datetime
import datetime

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from account.models import Organisation, Delivery, DeliveryAddress

# from account.models import Organisation
from files.models import Product
from files.pay import Robokassa
from .forms import NewOrder, ReportForm
from .models import Order, OrderItem, UtilsModel, StatusOrder
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

        delivery = Delivery.objects.get(id=delivery_id)
        logging.info(f"DELIVERY:  {delivery}")

        neworder = Order.objects.create(
            Contractor=form.user,
            date_complete=date_complite,
            # organisation_payer=organisation,
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
    logging.info(f'[info] тип данных возвращаемых формой наверняка строка?? {type(today)}--{today}')
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


def del_item_in_order(request, order_id: int, item_id: int):
    Orders = Order.objects.get(id=order_id)
    old_ord = OrderItem.objects.get(id=item_id)  # строка заказа
    print('PRODNUM', old_ord.product_id)
    product = Product.objects.get(id=old_ord.product_id)
    old_ord.delete()
    logging.info(f'[Удаляем из OrderItems] {old_ord}')

    product.delete()
    logging.info(f'[Удаляем из Product] {product}')
    # os.remove(f"media/{str(product.images)}")  # Удаление файла

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

    # --------------- Формирование счета---------
    # create_order_pdf.delay(order_id)
    # order_pdf = DrawOrder(order_id)  #
    # order_pdf.run()

    # _________________________Архивируем файлы для письма посылаем письмо с заказом------------------
    domain = str(get_domain(request))
    arh_for_mail.delay(order_id, domain=domain)
    # ------------Устанавливаем таймер на готовность заказа по истечении таймера отправлякем письмо с вопросом о готовности----------------
    # получаем дату готовности из базы

    start_count_down(domain, order_id)

    # -----------------------create_link_pay-----------------------------------
    Orders = Order.objects.get(id=order_id)
    user = request.user
    link_pay = Robokassa(Orders.total_price, f'Оплата заказа № {Orders.id}', order_id, user).run()
    # logger.info(f'Генерим платежную ссылку: ', link_pay)
    context = {"Orders": Orders, 'link_pay': link_pay}
    os.chdir(current_path)  # перейти обратно

    return render(request, "orderpay.html", context)


def start_count_down(domain, order_id):
    Orders = Order.objects.get(id=order_id)
    print('ДАТА ГОТОВНСТИ', Orders.date_complete)
    PeriodicTask.objects.create(
        name=f'Timer count Down order №{order_id}',
        task='timer_order_complete',
        # interval=IntervalSchedule.objects.get(every=1, period='hours'),
        interval=IntervalSchedule.objects.get(every=2, period='minutes'),
        args=json.dumps([order_id, domain]),
        # start_time=Orders.date_complete - datetime.timedelta(hours=3),  # за три часа до дедлайна пишем письма
        start_time=timezone.now() + datetime.timedelta(minutes=3),  # за три часа до дедлайна пишем письма

    )


def stop_count_down(order_id: int):
    '''Останавливаем отсылку писем с вопросами о готовности заказа'''
    item_periodic_task = PeriodicTask.objects.get(name=f'Timer count Down order №{order_id}')
    item_periodic_task.enabled = False
    item_periodic_task.save()
    item_periodic_task.delete()


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


def set_status_order(request, status_oder: int, pk: int, hash_code: str):
    ''' Подтверждение приема заказа менеджером типографии'''
    if hash_code == UtilsModel.calculate_signature(pk):  # Нужно проверить что хеш  равен коду от хеша номера заказа
        """Меняем статус заказа"""
        order = Order.objects.get(id=pk)  # получаем заказ по id заказаки
        status = StatusOrder.objects.get(id=status_oder)  # меняем статус заказа )  # меняю стаус
        logger.info(f"МЕНЯЮ СТАТУС нА В Работе")
        order.status = status
        order.save()

        return render(request, "files/confirm_order_to_work.html")
    else:
        return render(request, "files/no_confirm_order_to_work.html")
