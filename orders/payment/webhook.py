import json
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class WebHook:
    url_bank = 'https://enter.tochka.com/uapi/webhook/v1.0/'
    client_id = os.getenv('TOCHKA_CLIENT_ID')
    url_webhook_bank = url_bank + client_id
    url_webhook = os.getenv('WEBHOOK_URL')
    token = os.getenv('TOCHKA_TOKEN')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"

    }

    def get_webhook(self):
        payload = {}
        headers = self.headers
        response = requests.request("GET", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def create_webhook(self):
        # Создание веб хука
        # для адреса "url": "https://orders.san-cd.ru/orders/web_hook"
        payload = json.dumps({
            "webhooksList": [
                "incomingPayment"
            ],
            "url": self.url_webhook
        })
        headers = self.headers
        print(self.url_webhook_bank)
        print(payload)
        response = requests.request("PUT", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def edit_web_hook(self):
        payload = json.dumps({
            "webhooksList": [
                "incomingPayment"
            ],
            "url": self.url_webhook

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("POST", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def delete_web_hook(self):
        payload = {}
        headers = self.headers
        response = requests.request("DELETE", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    @classmethod
    def send_web_hook(cls):
        payload = json.dumps({
            "webhookType": "incomingPayment"
        })
        headers = cls.headers
        response = requests.request("POST", url=cls.url_webhook_bank + '/test_send', headers=headers, data=payload)
        print(response.text)


if __name__ == '__main__':
    # WebHook().get_webhook()
    # WebHook().delete_web_hook()
    # WebHook().create_webhook()
    WebHook.send_web_hook()
