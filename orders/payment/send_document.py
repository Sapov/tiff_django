import json

import requests

from orders.models import Order
from orders.payment import IdDocument
from orders.payment.bank import Bank


class SendDocument(Bank):
    def __get_user_email(self):
        order = Order.objects.get(id=self.order_id)
        return order.user.email

    def __create_payload(self):
        return json.dumps({
            "Data": {
                "email": self.__get_user_email()
            }
        })

    def send_invoice_to_email(self):
        document_id = IdDocument(self.order_id).get_base_document_id()
        url = f"{self.RS_URL}/invoice/{self.apiVersion}/bills/{self.customer_code}/{document_id}/email"
        payload = self.__create_payload()

        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)

    def send_closing_documents_to_email(self):
        document_id = IdDocument(self.order_id).get_base_document_id() # Тут нужно брать id акта
        payload = self.__create_payload()
        url = f"{self.RS_URL}/invoice/{self.apiVersion}/closing-documents/{self.customer_code}/{document_id}/email"
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)


