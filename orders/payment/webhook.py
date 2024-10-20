import json
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class WebHook:
    # url_bank = 'https://enter.tochka.com/uapi/webhook/v1.0/'

    url_bank = 'https://enter.tochka.com/sandbox/v2/webhook/v1.0/'
    client_id = os.getenv('TOCHKA_CLIENT_ID')
    url_webhook_bank = url_bank + client_id
    url_webhook = os.getenv('WEBHOOK_URL')
    token = 'working_token'

    def get_webhook(self):
        payload = {}
        headers = self.headers
        print(self.url_webhook_bank)
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
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.token}"

        }
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
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("DELETE", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def send_web_hook(self):
        payload = json.dumps({
            "webhookType": "incomingPayment"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("POST", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)


if __name__ == '__main__':
    # WebHook().get_webhook()
    hook = WebHook()
    hook.create_webhook()

