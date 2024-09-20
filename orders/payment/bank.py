import logging
from datetime import datetime, date
import json
import os
import requests
from dotenv import load_dotenv, find_dotenv

from mysite import settings
from orders.models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())


def goto_media_orders(foo):
    ''' переходим в папку media/orders и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
        curent_path = os.getcwd()
        os.chdir(
            f'{settings.MEDIA_ROOT}/orders/')
        logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
        res = foo(*args, **kwargs)
        os.chdir(curent_path)  # перейти обратно
        logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
        return res

    return wrapper


class Bank:
    # url = 'https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills'
    url = "https://enter.tochka.com/uapi/invoice/v1.0/bills"

    def __init__(self, order_id: int):
        self.document_id = None
        self.total_amount_order = 0
        self.order_id = order_id
        self.customer_code = None

    def create_invoice(self):
        payer = Order.objects.get(id=self.order_id)

        payload = json.dumps({
            "Data": {
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "customerCode": self.customer_code,
                "SecondSide": {
                    "accountId": f'{payer.organisation_payer.bank_account}/{payer.organisation_payer.bik_bank}',
                    "legalAddress": payer.organisation_payer.legalAddress,
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
        response = requests.request("POST", self.url, headers=headers, data=payload)
        logging.info(f'RESPONSE  {response}')
        self.document_id = response.json()['Data']['documentId']
        logging.info(f'document_id  {self.document_id}')

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

    @goto_media_orders
    def get_invoice(self):
        url = f"https://enter.tochka.com/uapi/invoice/v1.0/bills/{self.customer_code}/{self.document_id}/file"
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        with open(f'Order_{self.order_id}.pdf', 'wb') as file:
            file.write(response.content)

    def __get_customer_code(self):
        url = "https://enter.tochka.com/uapi/open-banking/v1.0/customers"
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.customer_code = response.json()['Data']['Customer'][0]['customerCode']
        logging.info(f'CUSTOMERCODE {self.customer_code}')

    def add_pdf_in_order(self):
        '''Записываем в таблицу ссылку на pdf счет с файлами'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'ADD PDF in order: orders/Order_{self.order_id}.pdf')
        order.order_pdf_file = f'orders/Order_{self.order_id}.pdf'
        order.save()

    def run(self):
        logging.info(f'ГЕНЕРИМ СЧЕТ ОТ БАНКА')
        self.__get_customer_code()
        self.create_invoice()
        self.get_invoice()
        self.add_pdf_in_order()
