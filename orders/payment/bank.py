import json
import os
import requests
from dotenv import load_dotenv, find_dotenv
from mysite import settings
from orders.models import Order, BankInvoices
import logging
from orders.payment import IdDocument
from .type.data import Data

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
    customer_code = os.getenv('CUSTOMER_COD')

    def __init__(self, order_id: int):
        self.document_id = None
        self.total_amount_order = 0
        self.order_id = order_id
        self.payer = Order.objects.get(id=self.order_id)

    def create_invoice(self):
        '''Выставляем счет'''
        self.__create_document('Invoice')
        self.__add_base_document_id()
        self.__get_invoice()
        self.__add_pdf_in_order()

    def create_act(self):
        self.url = self.RS_URL + f"/invoice/{self.apiVersion}/closing-documents"
        self.__create_document('Act')

    def __create_document(self, name_document: str):
        '''Генерируем Документ'''

        payload = json.dumps({
            "Data": Data(self.order_id).data(name_document)
        })
        logging.info(f'[DICT FOR DOCUMENT] {payload}')

        try:
            response = requests.request("POST", self.url, headers=self.headers, data=payload)
            logging.info(f'RESPONSE ORDER  {response.text}')
            self.document_id = response.json()['Data']['documentId']
            logging.info(f'СГЕНЕРИРОВАЛИ СЧЕТ ПОЛУЧИЛИ DOC ID {self.document_id}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error message create invoice {e}')

    def __add_base_document_id(self):
        IdDocument(self.order_id).add_base_document_id(self.document_id)

    @goto_media_orders
    def __get_invoice(self) -> None:

        url = f"{self.RS_URL}/invoice/{self.apiVersion}/bills/{self.customer_code}/{self.document_id}/file"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            with open(f'Order_{self.order_id}.pdf', 'wb') as file:
                file.write(response.content)
        except requests.exceptions.RequestException as e:
            logger.error(f' Error create PDF as {e}')

    def get_customer_code(self) -> str | None:
        '''
        https://developers.tochka.com/docs/tochka-api/api/get-customers-list-open-banking-v-1-0-customers-get
        '''

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

    def __add_pdf_in_order(self):
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

    def delete_invoice(self, order_id: int):
        document = BankInvoices.objects.get(order_id=order_id)
        url = f"{self.RS_URL}/invoice/v1.0/bills/{self.customer_code}/{document.document_id}"
        payload = {}
        response = requests.request("DELETE", url, headers=self.headers, data=payload)
        logging.info(f'[DELETING INVOICE]: {response.text}')
        print(response.text)

    def check_status_payment(self):
        '''
        При оповещегии об оплате через хук нужно проверить все не оплаченные документы на статус оплаты
        '''
        documents = BankInvoices.objects.filter(payment_Status=None)
