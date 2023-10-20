import hashlib
import os
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Pay:
    MerchantLogin = os.getenv("MERCHANT_LOGIN")
    password1 = os.getenv("PASSWORD_ONE")

    def __init__(self, received_sum: int, description: str, order_number: int):
        self.received_sum = received_sum
        self.description = description
        self.SignatureValue = None
        self.link = None
        self.order_number = order_number
        self.password = os.getenv("PASSWORD_ONE")

    def calculate_signature(self, *args) -> str:
        """Create signature MD5.
        """
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    def check_signature_result(self,
                               order_number: int,  # invoice number
                               received_sum: int,  # cost of goods, RU
                               received_signature: hex,  # SignatureValue
                               password: str  # Merchant password
                               ) -> bool:
        signature = self.calculate_signature(received_sum, order_number, password)
        if signature.lower() == received_signature.lower():
            return True
        return False

    def __generate(self):
        '''генерируем MD5 хеш для SignatureValue'''
        mystring = f'{self.MerchantLogin}:{self.received_sum}::{os.getenv("PASSWORD_ONE")}'
        hash_object = hashlib.md5(mystring.encode())
        self.SignatureValue = hash_object.hexdigest()
        logger.info(f'SignatureValue: {self.SignatureValue}')
        return self.SignatureValue

    def __create_pay_link(self):
        self.link = f'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={self.MerchantLogin}&OutSum={self.received_sum}&Description={self.description}&SignatureValue={self.SignatureValue}'
        logger.info(
            f'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={self.MerchantLogin}&OutSum={self.received_sum}&Description={self.description}&SignatureValue={self.SignatureValue}')
        return self.link

    def run(self):
        self.__generate()
        return self.__create_pay_link()


if __name__ == '__main__':
    print(Pay(100, 'печатьбаннера').run())
    print(Pay(100, 'печатьбаннера').calculate_signature(
        'MerchantLogin:self.received_sum:os.getenv("PASSWORD_ONE":1:Vasya'))


