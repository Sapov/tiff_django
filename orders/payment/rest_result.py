import json
import os
import requests
import logging
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())


class Acquiring:
    apiVersion = 'v1.0'
    RS_URL = "https://enter.tochka.com/uapi"
    AS_URL = "https://enter.tochka.com"
    url = RS_URL + f"/invoice/{apiVersion}/bills"

    headers: dict = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
    }

    def __init__(self, order_id: int):
        self.customer_code = None
        self.pay_link = None
        self.order_id = order_id
        self.terminalId = None
        self.merchantId = None
        self.total_amount_order = 0

    def get_retailers(self):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami#create_payment_operation_with_receipt_acquiring__apiVersion__payments_with_receipt_post'''
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/retailers?customerCode={self.customer_code}'
        payload = {}
        response = requests.request("GET", url, headers=self.headers, data=payload)
        logger.info(f'[RESPONSE JSON] {response.json()}')
        self.merchantId = (response.json()['Data']['Retailer'][0]['merchantId'])
        self.terminalId = (response.json()['Data']['Retailer'][0]['terminalId'])

        logger.info(f'MerchantId: {self.merchantId}')
        logger.info(f'TerminalId: {self.terminalId}')

    def create_payment_operation_with_receipt_link(self, organisation_flag):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami'''
        url_send_box = f'https://enter.tochka.com/sandbox/v2/acquiring/{self.apiVersion}/payments_with_receipt'
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/payments_with_receipt'

        # payer = Order.objects.get(id=self.order_id)

        if True:
            tel = '9515456824'
            payload = {
                "Data": {
                    "customerCode": self.customer_code,
                    "amount": '830',
                    "purpose": f"Оплата заказа № {2}",
                    "redirectUrl": "https://order.san-cd.ru/orders/success",
                    "failRedirectUrl": "https://order.san-cd.ru/orders/fail",
                    "paymentMode": ["sbp"],
                    "saveCard": True,
                    "consumerId": '',
                    "taxSystemCode": "usn_income",
                    "merchantId": self.merchantId,
                    "Client": {
                        "name": f'Александр' if organisation_flag
                        else 'Александр',
                        "email": 'forumvrn@gmail.com',

                        "phone": '+7999999999',
                    },
                    "Items": [{
                        "vatType": "none",
                        "name": "string",
                        "amount": "1234.00",
                        "quantity": 1,
                        "paymentMethod": "full_payment",
                        "paymentObject": "service",
                        "measure": "шт.",
                        "Supplier": {
                            "phone": "+7999999999",
                            "name": "ООО Альтер",
                            "taxCode": "660000000000"
                        }
                    }]
                }
            }
            try:
                response = requests.request("POST", url_send_box, headers=self.headers, data=json.dumps(payload))
                logger.info(f'RESPONSE FOR PAYMENT LINK :{response.json()}')
                print(response.json())

                # self.pay_link = response.json()['Data']['paymentLink']
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

        logger.info(f'Посчитанный TOTAL PRICE: {self.total_amount_order}')
        logger.info(f'positions: {positions}')

        return positions

    def check(self):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-razresheniyami#get_all_consents_list_consent__apiVersion__consents_get'''
        url = f"https://enter.tochka.com/uapi/{self.apiVersion}/consents"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            logger.info(f'response.text {response.text}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error as {e}')

    def _add_pay_link_in_table_order(self) -> None:
        '''Добавим ссылку об оплате в таблицу с ордером'''
        ''' добавим operationId'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'SAVE PAY-LINK: {self.pay_link}')
        order.pay_link = self.pay_link
        order.save()

    def get_customer_code(self) -> str | None:
        self.customer_code = os.getenv('CUSTOMER_COD')

    def run(self, organisation_flag) -> str:
        self.get_customer_code()
        logger.info(f'self.customer_code {type(self.customer_code)}')
        self.create_payment_operation_with_receipt_link(organisation_flag)
        return self.pay_link


if __name__ == '__main__':
    link_pay = Acquiring(order_id=2).run(organisation_flag=True)
    print(link_pay)
