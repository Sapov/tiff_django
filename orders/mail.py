from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Order


class Mail:
    def __init__(self, order_id: int, domain):
        self.domain = domain
        self.order_id = order_id

    def send_mail_request_for_order_readiness(self):
        """отправляем письмо с запросом о готовности заказа подрядчику"""
        order = Order.object.get(id=self.order_id)
        data = {
            "data_order_complete": order.order_complete,
            "confirm_status_complete": self.confirm_link_to_complited,
            "order_id": self.order_id,
        }

        html_message = render_to_string("mail/mail_order_for_typografyl.html", data)
        msg = EmailMultiAlternatives(
            subject=f"Готов ли заказ от REDS № {self.order_id}",
            to=[
                "rpk.reds@ya.ru",
            ],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
