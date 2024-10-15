from celery import shared_task

import users.whatssapp
from orders.models import UtilsModel
from .alerts import Alerts
from .payment.bank import Bank


@shared_task
def arh_for_mail(order_id: int, domain: str):
    order_item = UtilsModel(order_id, domain)
    order_item.run()


@shared_task(name='timer_order_complete')
def timer_order_complete(*args):
    order_id, domain = args
    print(f'[INFO]-------------Отсылаем письмо с вопросом о готовности заказа--№ {order_id}---------')
    item_mail = Alerts(order_id, domain)
    item_mail.send_mail_request_for_order_readiness()


@shared_task
def create_order_pdf(order_id):
    '''Формирования счета для организаций'''
    order = Bank(order_id)
    order.run()


@shared_task(name='check_payment_order')
def check_payment_order(*args):
    order_id, domain = args
    print(f'[INFO]-------------Проверяем оплату в банке--№ {order_id}---------')
    order = Bank(order_id)
    order.get_status_invoice()


@shared_task
def send_message_whatsapp(phone_number: str, text: str):
    '''Отсылаем сообщение в whatsapp'''
    users.whatssapp.send_message(phone_number, text)
