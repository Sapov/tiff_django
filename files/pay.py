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
        j = {"sno": "osn",  # = os.getenv('USN')
             "items": [
                 {
                     "name": self.description,
                     "quantity": 1,
                     "sum": self.received_sum,
                     "payment_method": "full_payment",
                     "payment_object": "commodity",
                     "tax": "vat10"
                 },
             ]
             }

        new_json = json.dumps(j, indent=2)
        return new_json
        # l = json.JSONEncoder

        '''
         {
          "sno":"osn",
          "items": [
            {
              "name": "Название товара 1",
              "quantity": 1,
              "sum": 100,
              "payment_method": "full_payment",
              "payment_object": "commodity",
              "tax": "vat10"
            },
            {
              "name": "Название товара 2",
              "quantity": 3,
              "sum": 450,
              "cost": 150,
              "payment_method": "full_prepayment",
              "payment_object": "service",
              "nomenclature_code": "04620034587217"
            }
          ]
        }



        '''

    def generate_payment_link(self,
                              is_test=0,
                              ) -> str:
        """URL for redirection of the customer to the service.
        """
        signature = self.calculate_signature(
            self.MerchantLogin,  # Merchant login
            self.received_sum,  # Cost of goods, RU
            self.order_number,  # Invoice number
            self.merchant_password_1  # Merchant password
        )

        data = {
            'MerchantLogin': self.MerchantLogin,
            'OutSum': self.received_sum,
            'InvId': self.order_number,
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
    test = Robokassa(100, 'Print banner', 1)
    # print(Robokassa(100, 'печать баннера', 1).generate_payment_link())
    print(test.generate_receipt())
