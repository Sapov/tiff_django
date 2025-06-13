import logging

import requests
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

HOST_URL = 'https://api.green-api.com/'
INSTANCE_URL = 'waInstance'
INSTANCE = os.getenv('GREENAPI_INSATANCE')
TOKEN = os.getenv('GREENAPI_TOKEN')


def send_message(phone_number: str, text: str):
    LOCAL_URL = 'sendMessage/'
    url = HOST_URL + INSTANCE_URL + INSTANCE + '/' + LOCAL_URL + TOKEN
    '''Отправка текстового сообщения на номер'''
    logger.info(f'[INFO] Отправляем сообщение {text} в WhatsApp на номер: {phone_number}')
    payload = {
        "chatId": f"{phone_number}@c.us",
        "message": text
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload)
    logger.info(f'[RESPONSE WHTASAPP SERVER]: {response.text.encode("utf8")}')


def send_document(phone_number: str, caption: str, files_path: str):
    '''Отправка документа на WHATSAPP'''
    LOCAL_URL = 'sendFileByUpload/'
    url = HOST_URL + INSTANCE_URL + INSTANCE + '/' + LOCAL_URL + TOKEN
    files = [
        ('file', ('47366255-1421606380.pdf', open(files_path, 'rb'), 'application/pdf'))
    ]
    payload = {
        "chatId": f"{phone_number}@c.us",
        'caption': caption,
        'fileName': 'window.pdf'
    }
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


if __name__ == '__main__':
    send_document('79802423868', 'Надпись...', '/home/sasha/47366255-1421606380.pdf')
