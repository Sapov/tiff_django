import decimal
import hashlib
import json
import os
import logging
from urllib import parse

logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Robokassa:
    '''Генерация ссылки на оплату для магазина'''
    MerchantLogin: str = os.getenv("MERCHANT_LOGIN")
    merchant_password_1: str = os.getenv("PASSWORD_ONE")
    robokassa_payment_url: str = 'https://auth.robokassa.ru/Merchant/Index.aspx'

    def __init__(self, received_sum: decimal, description: str, order_number: int):
        self.received_sum = received_sum
        self.description = description
        self.SignatureValue = None
        self.link = None
        self.order_number = order_number

    @classmethod
    def calculate_signature(cls, *args) -> str:
        """Create signature MD5.
        """
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    def generate_receipt(self):
        '''
        https://docs.robokassa.ru/fiscalization/
        '''
        j = {"sno": os.getenv('SNO'),  # система налогообложения
             "items": [
                 {
                     "name": self.description,
                     "quantity": 1,
                     "sum": self.received_sum,
                     "payment_method": "full_payment",
                     "payment_object": "commodity",
                     "tax": "none"
                 },
             ]
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
            'IsTest': is_test
        }
        return f'{self.robokassa_payment_url}?{parse.urlencode(data)}'

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

    def run(self):
        return self.__create_pay_link()


if __name__ == '__main__':
    # test = Robokassa(100, 'Print banner', 1)
    print(Robokassa(100, 'печать баннера', 1).generate_payment_link())
    # print(test.generate_receipt())
