from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Mail:

    def send_mail_request_for_order_readiness(self, order_id: int):
        """отправляем письмо с запросом о готовности заказа подрядчику"""
        data = {
            "data_order_complete": self.order_complete,
            "order_item": self.order_list,
            "confirm_status_complete": self.confirm_link_to_complited,
            "order_id": order_id,
        }

        html_message = render_to_string("mail/mail_order_for_typografyl.html", data)
        msg = EmailMultiAlternatives(
            subject=f"Готов ли заказ от REDS № {order_id}",
            to=[
                "rpk.reds@ya.ru",
            ],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
