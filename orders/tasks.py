from celery import shared_task

from files.works_with_files.atchives_files import UtilsModel
from .alerts import Alerts
from .payment.acquiring import Acquiring
from .payment.bank import Bank
from .email_sender.sender import EmailSender


@shared_task
def arh_for_mail(*args):
    order_item = UtilsModel(*args)
    order_item.run()


@shared_task(name='timer_order_complete')
def timer_order_complete(*args):
    print(f'[INFO]-------------Отсылаем письмо с вопросом о готовности заказа--№ {args[0]}---------')
    item_mail = Alerts(*args)
    item_mail.send_mail_request_for_order_readiness()


@shared_task
def create_order_pdf(order_id: int):
    '''Формирования счета для организаций'''
    document = Bank(order_id)
    document.create_invoice()

@shared_task()
def create_act(*args):
    '''Формирование закрывающего документа АКТ'''
    document = Bank(*args)
    document.create_act()

@shared_task
def create_pay_link_d(order_id: int, organisation: bool):
    '''Формирования ссылки для организаций и для физ лиц'''
    order = Acquiring(order_id)
    order.run(organisation)


@shared_task(name='check_payment_order')
def check_payment_order(*args):
    order_id, domain = args
    print(f'[INFO]-------------Проверяем оплату в банке--№ {order_id}---------')
    order = Bank(order_id)
    order.get_status_invoice()

@shared_task
# def send_mail_for_user(order_id, mail_address, order_pay_link):
def send_mail_for_user(*args):
    # mail = EmailSender(order_id, mail_address, order_pay_link)
    mail = EmailSender(*args)
    mail.send_mail()