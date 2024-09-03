import json
from datetime import date, datetime
import datetime


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import Order, UtilsModel
import logging

logger = logging.getLogger(__name__)


class Alerts:
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

        html_message = render_to_string("mail/mail_order_for_typography_alert_complete.html", data)
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

    @classmethod
    def start_count_down(cls, domain, order_id):
        Orders = Order.objects.get(id=order_id)
        print('ДАТА ГОТОВНСТИ', Orders.date_complete)
        PeriodicTask.objects.create(
            name=f'Timer count Down order №{order_id}',
            task='timer_order_complete',
            interval=IntervalSchedule.objects.get(every=1, period='hours'),
            # interval=IntervalSchedule.objects.get(every=2, period='minutes'),
            args=json.dumps([order_id, domain]),
            # start_time=Orders.date_complete - datetime.timedelta(hours=3),  # за три часа до дедлайна пишем письма
            start_time=timezone.now() + datetime.timedelta(minutes=3),  # за три часа до дедлайна пишем письма
        )
