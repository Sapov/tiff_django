# Create your tasks here


from celery import shared_task
from django.core.mail import send_mail

from orders.models import UtilsModel, Order
from orders.utils import DrawOrder, Utils


def send_mail_order(order_id, domain):
    """отправляем письмо с архивом подрядчику"""
    order = Order.objects.get(id=order_id)
    print('DOMAIN', domain)
    print('ID', order_id)
    print('ARHIVE', str(order.order_arhive))

    send_mail(
        "Новый заказ от REDS",
        # f'{self.new_str}\n',
        f"---\nCсылка на архив: http://{domain}/media/{str(order.order_arhive)}",
        "django.rpk@mail.ru",
        ["rpk.reds@ya.ru"],
        fail_silently=False,
    )


@shared_task
def arh_for_mail(order_id: int, domain: str):
    order_item = UtilsModel(order_id, domain)
    order_item.run()
    send_mail_order(order_id, domain)


@shared_task
def create_order_pdf(order_id):
    order_pdf = DrawOrder(order_id)  # Формирование счета
    order_pdf.run()
