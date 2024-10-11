import logging

import requests
import os

from django.contrib.auth import get_user_model
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)
User = get_user_model()
url = f"https://api.green-api.com/waInstance{os.getenv('GREENAPI_INSATANCE')}/sendMessage/{os.getenv('GREENAPI_TOKEN')}"


def send_message(user: str, text: str):
    item_user = User.objects.get(email=user)
    phone_number = item_user.phone_number
    print('FOR WAP',item_user, phone_number, item_user.whatsapp)
    if phone_number and item_user.whatsapp:
        logger.info(f'[INFO] Отправляем сообщение в WhatsApp на номер: {phone_number}')
        payload = {
            "chatId": f"{phone_number}@c.us",
            "message": text
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload)

        print(response.text.encode('utf8'))
