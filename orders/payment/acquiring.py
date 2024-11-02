import json
import os
import requests
# from orders.models import Order, OrderItem
from orders.payment.bank_tes import Bank


class Acquiring(Bank):
    headers: dict = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
    }

    def __init__(self, total_price: int, user: str, order_id: int):
        super().__init__(order_id)
        self.terminalId = None
        self.merchantId = None
        self.user = user
        self.total_price = total_price

    def get_retailers(self):
        url = f'https://enter.tochka.com/uapi/acquiring/v1.0/retailers?customerCode={self.customer_code}'

        # url = "https://enter.tochka.com/uapi/acquiring/v1.0/retailers?customerCode="

        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.status_code)
        print(response.json())
        self.merchantId = (response.json()['Data']['Retailer'][0]['merchantId'])
        self.terminalId = (response.json()['Data']['Retailer'][0]['terminalId'])
        print('self.merchantId', self.merchantId)
        print('self.terminalId', self.terminalId)

    def create_payment_link_with_receipt_test(self):
        # url = "https://enter.tochka.com/uapi/acquiring/v1.0/payments_with_receipt"
        url = 'https://enter.tochka.com/sandbox/v2/acquiring/v1.0/payments_with_receipt'
        # payer = Order.objects.get(id=self.order_id)

        payload = {
            "Data": {
                "customerCode": self.customer_code,
                "amount": 100,
                "purpose": f"Оплата заказа № ",
                "redirectUrl": "https://san-cd.ru",
                "failRedirectUrl": "https://san-cd.ru/fail",
                "paymentMode": [
                    "sbp",
                    "card"
                ],
                "saveCard": True,
                "consumerId": 'email@mail.ru',
                "taxSystemCode": "usn_income",
                "merchantId": self.merchantId,
                "Client": {
                    "name": 'Петр Петрович',  # self.user.first_name + self.user.last_name,
                    "email": 'test@mail.ru',
                    "phone": '79202423868',
                },
                "Items": self.__create_list_position_test()

            }
        }
        print(payload)
        response = requests.request("POST", url, headers=self.headers, data=json.dumps(payload))
        print(response.text)

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
                "paymentObject": "service",
                "measure": "шт."
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        return positions

    def __create_list_position_test(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        positions = []
        new_dict = {
            "vatType": "none",
            "name": f'Баннер 440 грамм 3х3  м',
            "amount": 100,
            "quantity": 1,
            "paymentMethod": "full_payment",
            "paymentObject": "service",
            "measure": "шт."
        }
        self.total_amount_order += 100
        positions.append(new_dict)

        return positions

    def a_run(self):
        super().get_customer_code()
        self.get_retailers()
        self.create_payment_link_with_receipt_test()
        # self.create_payment_link_with_receipt()


if __name__ == "__main__":
    t = Acquiring(123, 'sasha', 1)
    t.a_run()
