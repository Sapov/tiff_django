import os

from .second_side import SecondSide
from .content import Content
from .. import IdDocument
from ...models import Order


class Data:
    accountId = os.getenv('BANK_ACCOUNT_ID')
    customerCode = os.getenv('CUSTOMER_COD')

    def __init__(self, order_id: int):
        self.order_id = order_id
        self.payer = Order.objects.get(id=self.order_id)

    def data(self, name_document: str) -> dict[str:str]:
        if name_document == 'Invoice':
            return {'accountId': self.accountId,
                    'customerCode': self.customerCode,
                    'SecondSide': SecondSide(self.payer).__dict__,
                    'Content': Content(self.order_id).items_content(name_document)
                    }
        elif name_document == 'Act':
            return {'accountId': self.accountId,
                    'customerCode': self.customerCode,
                    'SecondSide': SecondSide(self.payer).__dict__,
                    'Content': Content(self.order_id).items_content(name_document),
                    "documentId": IdDocument(self.order_id).get_base_document_id()
                    }
