import logging

from orders.models import BankInvoices


class IdDocument:
    '''получение и запись ID document'''

    def __init__(self, order_id: int):
        self.order_id = order_id

    def add_base_document_id(self, document_id:str):
        BankInvoices.objects.get_or_create(order_id=self.order_id,
                                    document_id=document_id)
        logging.info(f'ЗАПИСАЛИ В БАЗУ ID document_ID: {document_id}')

    def get_base_document_id(self) -> int:
        return BankInvoices.objects.get(order_id = self.order_id).document_id