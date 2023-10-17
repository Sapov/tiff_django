import hashlib
import os
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Pay:
    MerchantLogin = os.getenv("MERCHANT_LOGIN")

    def __init__(self, summa: int, description: str):
        self.summa = summa
        self.description = description
        self.SignatureValue = None
        self.link = None

    def generate(self):
        '''генерируем MD5 хеш для SignatureValue'''
        mystring = f'{self.MerchantLogin}:{self.summa}::{os.getenv("PASSWORD_ONE")}'
        hash_object = hashlib.md5(mystring.encode())
        self.SignatureValue = hash_object.hexdigest()
        logger.info(f'SignatureValue: {self.SignatureValue}')

    def create_pay_link(self):
        self.link = f'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={self.MerchantLogin}&OutSum={self.summa}&Description={self.description}&SignatureValue={self.SignatureValue}'
        logger.info(
            f'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={self.MerchantLogin}&OutSum={self.summa}&Description={self.description}&SignatureValue={self.SignatureValue}')
        return self.link

    def run(self):
        self.generate()
        self.create_pay_link()


if __name__ == '__main__':
    print(Pay(100, 'печатьбаннера').run())
