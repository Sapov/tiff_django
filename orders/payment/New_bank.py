import json
import logging
import os
from datetime import datetime
import requests

from orders.models import Order, OrderItem


class Bank:
    apiVersion = 'v1.0'
    RS_URL = "https://enter.tochka.com/uapi"
    AS_URL = "https://enter.tochka.com"
    url = RS_URL + f"/invoice/{apiVersion}/bills"
    headers = {'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"}

    def __init__(self, order_id: int):
        self.document_id = None
        self.total_amount_order = 0
        self.order_id = order_id
        self.customer_code = os.getenv('CUSTOMER_COD')

    def create_invoice(self):
        payer = Order.objects.get(id=self.order_id)
        payload = json.dumps({
            "Data": {
                "customerCode": self.customer_code,
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "SecondSide": {
                    "accountId": f'{payer.organisation_payer.bank_account}/{payer.organisation_payer.bik_bank}',
                    "legalAddress": payer.organisation_payer.address,
                    "kpp": payer.organisation_payer.kpp,
                    "bankName": payer.organisation_payer.bank_name,
                    "bankCorrAccount": payer.organisation_payer.bankCorrAccount,
                    "taxCode": payer.organisation_payer.inn,
                    "type": 'ip' if len(payer.organisation_payer.inn) == 12 else 'company',
                    "secondSideName": payer.organisation_payer.name_full
                },
                "Content": {
                    "Invoice": {
                        "Positions": self.__create_list_position(),
                        "date": str(datetime.now().date()),
                        "totalAmount": self.total_amount_order,
                        "totalNds": "0",
                        "number": self.order_id,
                        # "basedOn": "Основание платежа",
                        # "comment": "Комментарий к платежу",
                    }
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        try:
            print('----PAYLOAD FOR Invoice----: ', payload)
            response = requests.request("POST", self.url, headers=headers, data=payload)
            logging.info(f'RESPONSE  {response}')
            self.document_id = response.json()['Data']['documentId']
            logging.info(f'СГЕНЕРИРОВАЛИ СЧЕТ ПОЛУЧИЛИ DOC ID {self.document_id}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error message create invoice {e}')

    def __create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            total_amount = v.price_per_item * v.product.quantity
            new_dict = {
                "positionName": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "unitCode": "шт.",
                "ndsKind": "without_nds",
                "price": float(v.product.price/v.product.quantity), #v.price_per_item,
                "quantity": v.product.quantity,
                "totalAmount": total_amount,
                "totalNds": 0
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        return positions



if __name__ == "__main__":
    print(Bank.headers)

    assert Bank.url == 'https://enter.tochka.com/uapi/invoice/v1.0/bills'