import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from orders.models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)


class EmailSender:
    TEMPLATE_MAIL_FOR_USER = "mail/template_for_usermail.html"

    def __init__(self, order_id: int, mail_address: str, order_pay_link:str):
        self.mail_address = mail_address
        self.order_id = order_id
        self.subject = 'Вы оформили заказ'
        self.order_pay_link = order_pay_link

    def send_mail(self):
        """отправляем письмо клиенту"""
        order = Order.objects.get(id=self.order_id)
        context = self.view_items_in_order(pk=self.order_id, order_pay_link = self.order_pay_link)

        data = {
            "data_order_complete": order.date_complete - datetime.timedelta(hours=24),  # Типог-я отдает на сутки раньше
            "order_id": self.order_id,
        }
        data.update(context)
        html_message = render_to_string(self.TEMPLATE_MAIL_FOR_USER, data)
        msg = EmailMultiAlternatives(
            subject=f"{self.subject} № {self.order_id}",
            to=[self.mail_address, ],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        logger.info(f'[INFO] отправил письмо клиенту на почту {self.mail_address}')

    @classmethod
    def view_items_in_order(cls, pk, order_pay_link):
        # отобразить файлы в заказе
        items_in_order = OrderItem.objects.filter(order=pk)  # файлы в заказе
        context = {
            "items_in_order": items_in_order,
            "order_id": pk,
            'order_pay_link': order_pay_link
        }
        return context
