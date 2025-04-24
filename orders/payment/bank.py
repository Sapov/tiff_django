from datetime import datetime, date
import json
import os

import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from dotenv import load_dotenv, find_dotenv
from django.utils import timezone

from mysite import settings
from orders.models import Order, OrderItem, BankInvoices
import logging

from orders.payment import IdDocument
from .type.second_side import SecondSide
from .type.content import Content
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
    apiVersion = 'v1.0'
    RS_URL = "https://enter.tochka.com/uapi"
    AS_URL = "https://enter.tochka.com"
    url = RS_URL + f"/invoice/{apiVersion}/bills"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
    }

    def __init__(self, order_id: int):
        self.document_id = None
        self.total_amount_order = 0
        self.order_id = order_id
        self.customer_code = os.getenv('CUSTOMER_COD')
        self.payer = Order.objects.get(id=self.order_id)


    def create_invoice(self):
        '''Генерируем счет'''

        logging.info(f'[INFO] payer {self.payer}')

        payload = json.dumps({
            "Data": {
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "customerCode": self.customer_code,
                "SecondSide": SecondSide(self.payer).__dict__,

                "Content": Content(self.order_id).items_content('Invoice')
                #     {
                #     "Invoice": {
                #         "Positions": self.create_list_position(),
                #         "date": str(datetime.now().date()),
                #         "totalAmount": self.total_amount_order,
                #         "totalNds": "0",
                #         "number": str(self.order_id),
                #         # "basedOn": "Основание платежа",
                #         # "comment": "Комментарий к платежу",
                #     }
                # }
            }
        })
        logging.info(f'[dict] {payload}')

        # payload = json.dumps(di)

        try:
            logging.info(f'[PAYLOAD FOR Invoice] : {payload}')
            response = requests.request("POST", self.url, headers=self.headers, data=payload)
            logging.info(f'RESPONSE ORDER  {response.text}')
            self.document_id = response.json()['Data']['documentId']
            logging.info(f'СГЕНЕРИРОВАЛИ СЧЕТ ПОЛУЧИЛИ DOC ID {self.document_id}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error message create invoice {e}')

    def __add_base_document_id(self):
        IdDocument(self.order_id).add_base_document_id(self.document_id)

    def create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            total_amount = v.price_per_item  #
            new_dict = {
                "positionName": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "unitCode": "шт.",
                "ndsKind": "without_nds",
                "price": float(v.product.price / v.product.quantity),
                "quantity": v.product.quantity,
                "totalAmount": total_amount,
                "totalNds": 0
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        return positions

    @goto_media_orders
    def get_invoice(self) -> None:

        url = f"{self.RS_URL}/invoice/{self.apiVersion}/bills/{self.customer_code}/{self.document_id}/file"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            with open(f'Order_{self.order_id}.pdf', 'wb') as file:
                file.write(response.content)
        except requests.exceptions.RequestException as e:
            logger.error(f' Error create PDF as {e}')

    def get_customer_code(self) -> str | None:

        url = f"{self.RS_URL}/open-banking/{self.apiVersion}/customers"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            self.customer_code = response.json()['Data']['Customer'][0]['customerCode']
            logging.info(f'RESPONSE__CUSTOMER_ID: {self.customer_code}')
            return self.customer_code
        except requests.exceptions.RequestException as e:
            print(f'ERROR sending message: {e}')
            logger.error(f'ERROR sending messag: {e}')

    def add_pdf_in_order(self):
        '''Записываем в таблицу ссылку на pdf счет с файлами'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'ADD PDF in order: orders/Order_{self.order_id}.pdf')
        order.order_pdf_file = f'orders/Order_{self.order_id}.pdf'
        order.save()

    def get_status_invoice(self):
        '''https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-vystavleniem-schetov#get_invoice_invoice__apiVersion__bills__customerCode___documentId__file_get'''
        document = BankInvoices.objects.get(order_id=self.order_id)
        url = f'{self.RS_URL}/invoice/{self.apiVersion}/bills/{self.customer_code}/{document.document_id}/payment-status'

        payload = ""
        response = requests.request("GET", url, headers=self.headers, data=payload)
        logger.info(response.text)
        payment_status = response.json()['Data']['paymentStatus']
        logging.info(f'PAYMENT STATUS {payment_status}')
        document.payment_Status = payment_status
        document.save()

    @classmethod
    def check_payment(cls, domain, order_id):
        '''Запускаем ежечасную проверку оплаты '''
        PeriodicTask.objects.create(
            name=f'Check payment order №{order_id}',
            task='check_payment_order',
            interval=IntervalSchedule.objects.get(every=1, period='hours'),
            # interval=IntervalSchedule.objects.get(every=2, period='minutes'),
            args=json.dumps([order_id, domain]),
            start_time=timezone.now()
        )

    def delete_invoice(self, order_id: int):
        document = BankInvoices.objects.get(order_id=order_id)
        url = f"{self.RS_URL}/invoice/v1.0/bills/{self.customer_code}/{document.document_id}"
        payload = {}
        response = requests.request("DELETE", url, headers=self.headers, data=payload)
        logging.info(f'[DELETING INVOICE]: {response.text}')
        print(response.text)

    def check_status_payment(self):
        '''проверка всех счетов имеющих статус не оплачено'''
        documents = BankInvoices.objects.filter(payment_Status=None)


    def run(self):
        # self.get_customer_code()
        self.create_invoice()
        self.__add_base_document_id()
        self.get_invoice()
        self.add_pdf_in_order()


if __name__ == '__main__':
    a = Bank(3)
    a.get_customer_code()
