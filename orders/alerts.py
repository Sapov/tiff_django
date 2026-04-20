import json
from datetime import datetime
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import Order, OrderItem
from files.works_with_files.atchives_files import UtilsModel
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
        self.__generate_link_add_time_order()
        context = self.view_items_in_order(pk=self.order_id)

        data = {
            "data_order_complete": order.date_complete - datetime.timedelta(hours=24),  # Типог-я отдает на сутки раньше
            "confirm_status_complete": self.confirm_link_to_completed,
            "order_id": self.order_id,
            "add_time_order": self.add_time_order,
        }
        data.update(context)
        html_message = render_to_string("mail/mail_order_for_typography_alert_complete.html", data)
        msg = EmailMultiAlternatives(
            subject=f"Подтвердите готовность заказа № {self.order_id}",
            to=[
                "rpk.reds@ya.ru",
            ],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()


    def __generate_link_to_completed(self):
        '''Генерирую ссылку с уникальным ключом для перевода заказа в состояние в готов'''
        self.confirm_link_to_completed = (f'http://{self.domain}/confirm_order_to_competed/{self.order_id}/'
                                          f'{UtilsModel.calculate_signature(self.order_id)}')
        logger.info(f'[Генерирую ссылку ПЕРЕВОД С СОСТОЯНИЕ ГОТОВ] CONFIRM LINK: {self.confirm_link_to_completed}')

    def __generate_link_add_time_order(self):
        self.add_time_order = (f'http://{self.domain}/add_time_order/{self.order_id}/'
                               f'{UtilsModel.calculate_signature(self.order_id)}')
        logger.info(f'[Генерирую ссылку Добавочное время] : {self.add_time_order}')

    @classmethod
    def start_count_down(cls, domain, order_id: int):
        '''Не присылать письма во вне рабочее время'''
        order = Order.objects.get(id=order_id)
        logger.info(f'Старт обратного отсчета ДАТА ГОТОВНОСТИ, {order.date_complete}')
        # if not PeriodicTask.objects.get(name=f'Timer count Down order №{order_id}'):

        PeriodicTask.objects.create(
            name=f'Timer count Down order №{order_id}',
            task='timer_order_complete',
            interval=IntervalSchedule.objects.get(every=1, period='hours'),
            # interval=IntervalSchedule.objects.get(every=2, period='minutes'),
            args=json.dumps([order_id, domain]),
            start_time=order.date_complete - datetime.timedelta(hours=24),  # оповестить за 24 до дедлайна
        )

    @classmethod
    def set_time_count_down(cls, order_id: int, domain):
        """
        @param order_id: номер заказа
        @param domain: домен
        """
        cls.stop_count_down(order_id)
        order = Order.objects.get(id=order_id)
        PeriodicTask.objects.create(
            name=f'Timer count Down order №{order_id}',
            task='timer_order_complete',
            interval=IntervalSchedule.objects.get(every=1, period='hours'),
            args=json.dumps([order_id, domain]),
            start_time=order.date_complete - datetime.timedelta(hours=1),  # ЗА час до дедлайна
        )

    @classmethod
    def stop_count_down(cls, order_id: int):
        '''Останавливаем отсылку писем с вопросами о готовности заказа'''
        try:
            item_periodic_task = PeriodicTask.objects.get(name=f'Timer count Down order №{order_id}')
            item_periodic_task.enabled = False
            item_periodic_task.save()
            item_periodic_task.delete()
        except Exception as Ex:
            print('Нет уже задачи', Ex)

    @classmethod
    def view_items_in_order(cls, pk):
        # отобразить файлы в заказе
        items_in_order = OrderItem.objects.filter(order=pk)  # файлы в заказе
        context = {
            "items_in_order": items_in_order,
            "order_id": pk,
        }
        return context
