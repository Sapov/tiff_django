import decimal
import hashlib
import json
import os
import logging
from urllib import parse

from orders.models import OrderItem, Order

logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Robokassa:
    '''Генерация ссылки на оплату для магазина'''
    MerchantLogin: str = os.getenv("MERCHANT_LOGIN")
    merchant_password_1: str = os.getenv("PASSWORD_ONE")
    robokassa_payment_url: str = 'https://auth.robokassa.ru/Merchant/Index.aspx'

    def __init__(self, received_sum: decimal, description: str, order_number: int, user: str):
        self.received_sum = received_sum
        self.description = description
        self.SignatureValue = None
        self.pay_link = None
        self.order_number = order_number
        self.user = user

    @classmethod
    def calculate_signature(cls, *args) -> str:
        """Create signature MD5.
        """
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    def resept(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_number)
        list_items = []
        for i, v in enumerate(order_items):
            new_dict = {
                "name": f'{v.product.material} {v.product.length}x{v.product.width} см',
                "quantity": v.product.quantity,
                "sum": v.price_per_item,
                "payment_method": "full_payment",
                "payment_object": "commodity",
                "tax": "none"
            }
            list_items.append(new_dict)
        print(list_items)
        return list_items

    def generate_receipt(self):
        '''
        https://docs.robokassa.ru/fiscalization/
        Формируем все позиции заказа в робочек
        '''
        list_items = self.resept()
        j = {"sno": os.getenv('SNO'),  # система налогообложения
             "items": list_items
             }

        new_json = json.dumps(j, indent=2)
        return new_json

    def generate_payment_link(self,
                              is_test=0,
                              ) -> str:
        """URL for redirection of the customer to the service.
        """
        reciept = self.generate_receipt()
        signature = self.calculate_signature(
            self.MerchantLogin,  # Merchant login
            self.received_sum,  # Cost of goods, RU
            self.order_number,  # Invoice number
            reciept,  # Receipt
            self.merchant_password_1  # Merchant password
        )

        data = {
            'MerchantLogin': self.MerchantLogin,
            'OutSum': self.received_sum,
            'InvId': self.order_number,
            'Receipt': reciept,
            'Description': self.description,  # Description of the purchase
            'SignatureValue': signature,
            'IsTest': is_test,
            'Email': self.user

        }
        self.pay_link = f'{self.robokassa_payment_url}?{parse.urlencode(data)}'
        self._add_pay_link_in_table_order()  # добавляем ссылку в базу
        return self.pay_link

    # def check_signature_result(self,
    #                            order_number: int,  # invoice number
    #                            received_sum: int,  # cost of goods, RU
    #                            received_signature: hex,  # SignatureValue
    #                            password: str  # Merchant password
    #                            ) -> bool:
    #     signature = calculate_signature(received_sum, order_number, password)
    #     if signature.lower() == received_signature.lower():
    #         return True
    #     return False
    def _add_pay_link_in_table_order(self):
        '''Добавим ссылку об оплате в таблицу с ордером'''
        order = Order.objects.get(id=self.order_number)
        print(f'SAVE PAYLINK: {self.pay_link}')
        order.pay_link = self.pay_link
        order.save()

    def run(self):
        return self.generate_payment_link()


if __name__ == '__main__':
    test = Robokassa(100, 'Print banner', 1)
    print(test.generate_receipt())
