import os

import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Bank:
    url = 'https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills'

    def create_bank_order(self):
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
