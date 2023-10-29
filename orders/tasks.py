# Create your tasks here


from celery import shared_task
from django.core.mail import send_mail

from orders.models import UtilsModel, Order
from orders.utils import DrawOrder, Utils


@shared_task
def arh_for_mail(order_id: int, domain: str):
    order_item = UtilsModel(order_id, domain)
    order_item.run()
    # send_mail_order(order_id, domain)


@shared_task
def create_order_pdf(order_id):
    order_pdf = DrawOrder(order_id)  # Формирование счета
    order_pdf.run()
