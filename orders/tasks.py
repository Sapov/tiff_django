# Create your tasks here


from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives

from orders.models import UtilsModel, Order
from orders.utils import DrawOrder, Utils
from django.template.loader import render_to_string


@shared_task
def arh_for_mail(order_id: int, domain: str):
    """Отправляем письмо подрядчику"""
    order_item = UtilsModel(order_id, domain)
    order_item.run()


@shared_task
def feedback_mail(cleaned_data):
    data = {"message": cleaned_data["message"], "phone": cleaned_data["phone"]}
    """Отправляем письмо себе"""
    # send_mail(
    #     f"Письмишко с сайта",
    #     # f'{self.new_str}\n',
    #     f"{cleaned_data['message']}\n",
    #     "django.rpk@mail.ru",
    #     [f"rpk.reds@ya.ru"],
    #     html_message=render_to_string("info/index.html", data),
    #     fail_silently=False,
    # )

    html_message = render_to_string("info/new_order_mail.html", data)
    msg = EmailMultiAlternatives(
        subject="еbmbmbма",
        to=[
            "rpk.reds@ya.ru",
        ],
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()


# @shared_task
# def create_order_pdf(order_id):
#'''Формирования счета для организаций'''
#     order_pdf = DrawOrder(order_id)  # Формирование счета
#     order_pdf.run()
