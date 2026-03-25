import json
import os
import requests
import logging
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


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
        self.payer = Order.objects.get(id=self.order_id)

    def get_customer_code(self) -> str | None:

        url = f"{self.RS_URL}/open-banking/{self.apiVersion}/customers"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            print(response.text)
            self.customer_code = response.json()['Data']['Customer'][0]['customerCode']
            logging.info(f'GET_CUSTOMER_ID: {self.customer_code}')
            print(f'----------RESPONSE__CUSTOMER_ID: {self.customer_code}')
            return self.customer_code
        except requests.exceptions.RequestException as e:
            print(f'ERROR get custom code message: {e}')
            logger.error(f'ERROR get custom code: {e}')

    def __add_pdf_in_order(self):
        '''Записываем в таблицу ссылку на pdf счет с файлами'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'ADD PDF in order: orders/Order_{self.order_id}.pdf')
        order.order_pdf_file = f'orders/Order_{self.order_id}.pdf'
        order.save()


class Acquiring(Bank):
    headers: dict = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
    }

    def __init__(self, order_id: int):
        self.pay_link = None
        self.order_id = order_id
        self.terminalId = None
        self.merchantId = None
        self.total_amount_order = 0

    def create_payment_operation_with_receipt_link(self, organisation_flag):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami'''
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/payments_with_receipt'
        # url = f'https://enter.tochka.com/sandbox/v2/acquiring/v1.0/payments_with_receipt'
        if True:
            tel = '+79852325588'
            payload = {
                "Data": {
                    "customerCode": self.customer_code,
                    "amount": '12800.0',
                    "purpose": "Оплата заказа № 51",
                    "redirectUrl": "https://order.san-cd.ru/orders/success",
                    "failRedirectUrl": "https://order.san-cd.ru/orders/fail",
                    "paymentMode": [
                        "sbp",
                        "card",

                    ],
                    "saveCard": True,
                    # "consumerId": "rpk.reds@yandex.ru",
                    "taxSystemCode": "usn_income",
                    "Client": {
                        "name": "\u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440",
                        "email": "rpk.reds@yandex.ru",
                        "phone": "+79802423868"
                    },
                    "Items": [
                        {
                            "vatType": "none",
                            "name": "\u041f\u0435\u0447\u0430\u0442\u044c \u043d\u0430 \u041f\u0412\u0425 3 \u043c\u043c UV-\u043f\u0435\u0447\u0430\u0442\u044c 1.0x3.0 \u043c",
                            "amount": '12800.0',
                            "quantity": 1,
                            "paymentMethod": "full_payment",
                            "paymentObject": "goods",
                            "measure": "\u0448\u0442."
                        }
                    ]
                }
            }
            # print('PAYLOAD', json.dumps(payload, indent=4))
            try:
                response = requests.request("POST", url, headers=self.headers, data=json.dumps(payload))
                print('RESPONSE FOR PAYMENT LINK', response.json())
                self.pay_link = response.json()['Data']['paymentLink']
                # self._add_pay_link_in_table_order()
            except requests.exceptions.RequestException as e:
                logger.error(f' Error create payment link {e}')

    def __create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            total_amount = v.product.price  # * v.product.quantity
            new_dict = {
                "vatType": "none",
                "name": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "amount": float(v.product.price / v.product.quantity),
                "quantity": v.product.quantity,
                "paymentMethod": "full_payment",
                "paymentObject": "goods",
                "measure": "шт."
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        print(f'Посчитанный тотал pice {self.total_amount_order}')
        print('positions', positions)
        return positions

    def check(self):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-razresheniyami#get_all_consents_list_consent__apiVersion__consents_get'''
        url = f"https://enter.tochka.com/uapi/{self.apiVersion}/consents"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            print(response.text)
        except requests.exceptions.RequestException as e:
            logger.error(f'Error as {e}')

    def _add_pay_link_in_table_order(self) -> None:
        '''Добавим ссылку об оплате в таблицу с ордером'''
        ''' добавим operationId'''
        order = Order.objects.get(id=self.order_id)
        print(f'SAVE PAY-LINK: {self.pay_link}')
        order.pay_link = self.pay_link
        order.save()

    def run(self, organisation_flag) -> str:
        super().get_customer_code()
        self.create_payment_operation_with_receipt_link(organisation_flag)
        return self.pay_link



if __name__ == '__main__':
    items = Acquiring(order_id=2)
    items.run(organisation_flag=False)