from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Order, UtilsModel
import logging

logger = logging.getLogger(__name__)


class Mail:
    def __init__(self, order_id: int, domain):
        self.domain = domain
        self.order_id = order_id

    def send_mail_request_for_order_readiness(self):
        """отправляем письмо с запросом о готовности заказа подрядчику"""
        order = Order.objects.get(id=self.order_id)
        self.__generate_link_to_completed()
        data = {
            "data_order_complete": order.date_complete,
            "confirm_status_complete": self.confirm_link_to_completed,
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

    def __generate_link_to_completed(self):
        '''Генерирую ссылку с уникальным ключом для перевода заказа в состояние в готов'''
        self.confirm_link_to_completed = (f'http://{self.domain}/files/confirm_order_to_competed/{self.order_id}/'
                                          f'{UtilsModel.calculate_signature(self.order_id)}')
        logger.info(f'[Генерирую ссылку ПЕРЕВОД С СОСТОЯНИЕ ГОТОВ] CONFIRM LINK: {self.confirm_link_to_completed}')
