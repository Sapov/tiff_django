import os

import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Bank:
    url = 'https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills'
    customerCode = '300000092'
    documentId = ''
    url_get = "https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills/300000092/1cf95c4f-e794-4407-bac4-0829f19bd2be/file"

    def create_invoice(self):
        payload = json.dumps({
            "Data": {
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "customerCode": "300000092",
                "SecondSide": {
                    "accountId": "40817810802000000008/044525104",
                    "legalAddress": "624205, РОССИЯ, СВЕРДЛОВСКАЯ обл, ЛЕСНОЙ г, ЛЕНИНА ул, ДОМ 96, офис КВ. 19",
                    "kpp": "668101001",
                    "bankName": "ООО БАНК ТОЧКА",
                    "bankCorrAccount": "30101810745374525104",
                    "taxCode": "660000000000",
                    "type": "company",
                    "secondSideName": "ООО Студия дизайна М-АРТ"
                },
                "Content": {
                    "Invoice": {
                        "Positions": [
                            {
                                "positionName": "Название товара",
                                "unitCode": "шт.",
                                "ndsKind": "nds_0",
                                "price": "1234.56",
                                "quantity": "1234.567",
                                "totalAmount": "1234.56",
                                "totalNds": "1234.56"
                            }
                        ],
                        "date": "2010-10-29",
                        "totalAmount": "1234.56",
                        "totalNds": "1234.56",
                        "number": "1",
                        "basedOn": "Основание платежа",
                        "comment": "Комментарий к платежу",
                        "paymentExpiryDate": "2020-01-20"
                    }
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer working_token'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        print(response.text)

    def get_invoice(self):
        url = "https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills/300000092/da408a57-bcfa-404c-8f2f-64446a1fa0ba/file"
        # da408a57-bcfa-404c-8f2f-64446a1fa0ba
        payload = {}
        headers = {
            'Authorization': 'Bearer working_token'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        with open('test.pdf', 'wb') as file:
            file.write(response.content)

    def get_customers_list(self):
        url = "https://enter.tochka.com/uapi/open-banking/v1.0/customers"
        payload = {}
        headers = {
            'Authorization': 'Bearer <token>'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)


if __name__ == '__main__':
    order = Bank()
    # order.create_invoice()
    order.get_invoice()
    # order.get_customers_list()
