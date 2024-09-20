from celery import shared_task
from orders.models import UtilsModel
from .alerts import Alerts
from .payment.bank import Bank


@shared_task
def arh_for_mail(order_id: int, domain: str):
    order_item = UtilsModel(order_id, domain)
    order_item.run()
    # send_mail_order(order_id, domain)


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
