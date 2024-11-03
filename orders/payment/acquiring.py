import json
import os
import requests
from orders.models import Order, OrderItem
from orders.payment.bank_tes import Bank


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

    def get_retailers(self):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami#create_payment_operation_with_receipt_acquiring__apiVersion__payments_with_receipt_post'''
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/retailers?customerCode={self.customer_code}'
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.json())
        self.merchantId = (response.json()['Data']['Retailer'][0]['merchantId'])
        self.terminalId = (response.json()['Data']['Retailer'][0]['terminalId'])
        print('self.merchantId', self.merchantId)
        print('self.terminalId', self.terminalId)

    def create_payment_operation_with_receipt_link(self, organisation_flag):
        ''' https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami'''
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/payments_with_receipt'
        payer = Order.objects.get(id=self.order_id)

        payload = {
            "Data": {
                "customerCode": self.customer_code,
                "amount": payer.total_price,
                "purpose": f"Оплата заказа № {payer.id}",
                "redirectUrl": "https://san-cd.ru/orders/success",
                "failRedirectUrl": "https://san-cd.ru/orders/fail",
                "paymentMode": [
                    "sbp",
                    "card"
                ],
                "saveCard": True,
                "consumerId": str(payer.Contractor),
                "taxSystemCode": "usn_income",
                "merchantId": self.merchantId,
                "Client": {
                    "name": f'{str(payer.Contractor.first_name)} {payer.Contractor.last_name}' if organisation_flag else str(
                        payer.organisation_payer),
                    "email": str(payer.Contractor),
                    "phone": f"+7{payer.Contractor.phone_number.national_number}",
                },
                "Items": self.__create_list_position()
            }
        }
        print('PAYLOAD', json.dumps(payload, indent=4))
        response = requests.request("POST", url, headers=self.headers, data=json.dumps(payload))
        print(response.json())
        self.pay_link = response.json()['Data']['paymentLink']
        self._add_pay_link_in_table_order()

    def __create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            total_amount = v.price_per_item * v.product.quantity
            new_dict = {
                "vatType": "none",
                "name": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "amount": v.price_per_item,
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
        response = requests.request("GET", url, headers=self.headers, data=payload)
        print(response.text)

    def create_payment_operation(self):
        '''https://enter.tochka.com/doc/v2/redoc/tag/Rabota-s-platyozhnymi-ssylkami#get_payment_operation_list_acquiring__apiVersion__payments_get'''
        url = f'https://enter.tochka.com/uapi/acquiring/{self.apiVersion}/payments'
        payload = {
            "Data": {
                "customerCode": self.customer_code,
                "amount": "1234.00",
                "purpose": "Перевод за оказанные услуги",
                "redirectUrl": "https://example.com",
                "failRedirectUrl": "https://example.com/fail",
                "paymentMode": [
                    "sbp",
                    "card"
                ],
                "saveCard": True,
                "consumerId": "fedac807-078d-45ac-a43b-5c01c57edbf8"
            }
        }
        response = requests.request("POST", url, headers=self.headers, data=json.dumps(payload))
        print(response.text)

    def _add_pay_link_in_table_order(self) -> None:
        '''Добавим ссылку об оплате в таблицу с ордером'''
        order = Order.objects.get(id=self.order_id)
        print(f'SAVE PAY-LINK: {self.pay_link}')
        order.pay_link = self.pay_link
        order.save()

    def run(self, organisation_flag) -> str:
        super().get_customer_code()
        self.create_payment_operation_with_receipt_link(organisation_flag)
        return self.pay_link
        # self.get_retailers()
        # self.check()


if __name__ == "__main__":
    t = Acquiring(123, 'sasha', 1)
    t.run()
