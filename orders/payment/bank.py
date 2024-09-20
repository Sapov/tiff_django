from datetime import datetime

import json
import os

import requests
from dotenv import load_dotenv, find_dotenv

from orders.models import Order, OrderItem

load_dotenv(find_dotenv())


class Bank:
    url = 'https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills'
    documentId = ''
    url_get = "https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills/300000092/1cf95c4f-e794-4407-bac4-0829f19bd2be/file"

    def __init__(self, order_id: int):
        self.total_amount_order = 0
        self.order_id = order_id

    def create_invoice(self):
        payer = Order.objects.get(id=self.order_id)

        payload = json.dumps({
            "Data": {
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "customerCode": self.__get_customer_code(),
                "SecondSide": {
                    "accountId": f'{payer.organisation_payer.bank_account}/{payer.organisation_payer.bik_bank}',
                    "legalAddress": payer.organisation_payer.legalAddress, #"624205, РОССИЯ, СВЕРДЛОВСКАЯ обл, ЛЕСНОЙ г, ЛЕНИНА ул, ДОМ 96, офис КВ. 19",
                    "kpp": payer.organisation_payer.kpp,
                    "bankName": payer.organisation_payer.bank_name,
                    "bankCorrAccount": payer.organisation_payer.bankCorrAccount,
                    "taxCode": payer.organisation_payer.tax_сode,
                    "type": "company",
                    "secondSideName": payer.organisation_payer.name_ul
                },
                "Content": {
                    "Invoice": {
                        "Positions": self.__create_list_position(),
                        # [
                        #     {
                        #         "positionName": "Название товара",
                        #         "unitCode": "шт.",
                        #         "ndsKind": "nds_0",
                        #         "price": "1234.56",
                        #         "quantity": "1234.567",
                        #         "totalAmount": "1234.56",
                        #         "totalNds": "1234.56"
                        #     }
                        # ],
                        "date": str(datetime.now().date()),
                        "totalAmount": self.total_amount_order,
                        "totalNds": "0",
                        "number": self.order_id,
                        "basedOn": "Основание платежа",
                        "comment": "Комментарий к платежу",
                    }
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer working_token'
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        print(response.text)

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
                "price": v.price_per_item,
                "quantity": v.product.quantity,
                "totalAmount": total_amount,
                "totalNds": 0
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        return positions

    def get_invoice(self):
        url = "https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills/300000092/da408a57-bcfa-404c-8f2f-64446a1fa0ba/file"
        # da408a57-bcfa-404c-8f2f-64446a1fa0ba
        payload = {}
        headers = {
            'Authorization': 'Bearer working_token'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        with open('test.pdf', 'wb') as file:
            file.write(response.content)

    def __get_customer_code(self):
        url = "https://enter.tochka.com/uapi/open-banking/v1.0/customers"
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print('CustomerCODE', response.text)
        print(response.json()['Data']['Customer'][0]['customerCode'])
        customer_code = response.json()['Data']['Customer'][0]['customerCode']
        return customer_code

    def run(self):
        self.create_invoice()



