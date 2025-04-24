from datetime import datetime

import requests
import json

from orders.payment import IdDocument
from orders.payment.bank import Bank
from orders.payment.type.second_side import SecondSide


class BankCloseDocument(Bank):
    '''https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-zakryvayushimi-dokumentami'''
    RS_URL = super().RS_URL
    apiVersion = super().apiVersion
    url = RS_URL + f"/invoice/{apiVersion}/closing-documents"
    headers = super().headers
    customer_code = super().customer_code
    aaa = Bank.RS_URL

    def close_document(self):
        payload = json.dumps({
            "Data": {
                "customerCode": self.customer_code,
                "accountId": "40817810802000000008/044525104",
                "documentId": IdDocument(self.order_id).get_base_document_id(),
                "Content": {
                    "Act": {
                        "number": self.order_id,
                        # "basedOn": "Основание платежа", !!! оферта сайта
                        # "comment": "Комментарий",
                        "date": str(datetime.now().date()),
                        "totalAmount": super().total_amount_order,
                        "totalNds": "0",
                        "Positions": self.create_list_position()
                    }
                },
                "SecondSide": SecondSide(self.payer).__dict__

            }
        })
        headers = {
            'Authorization': 'Bearer <token>',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    if __name__ == "__main__":
        main()
