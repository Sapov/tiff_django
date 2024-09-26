import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
url = f"https://api.green-api.com/waInstance{os.getenv('GREENAPI_INSATANCE')}/sendMessage/{os.getenv('GREENAPI_TOKEN')}"


def send_message(text: str):
    payload = {
        "chatId": f"{os.getenv('PHONE_NUMBER')}@c.us",
        "message": text
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload)

    print(response.text.encode('utf8'))


send_message('Текст сообщения')
