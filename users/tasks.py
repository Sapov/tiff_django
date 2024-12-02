from celery import shared_task

import users.whatssapp


@shared_task
def send_message_whatsapp(phone_number: str, text: str):
    '''Отсылаем сообщение в whatsapp'''
    users.whatssapp.send_message(phone_number, text)
