import requests
import json

from orders.payment.bank import Bank


class BankCloseDocument(Bank):
    RS_URL = super().RS_URL
    apiVersion = super().apiVersion
    url = RS_URL + f"/invoice/{apiVersion}/closing-documents"
    headers = super().headers

    payload = json.dumps({
        "Data": {
            "customerCode": "300000092",
            "accountId": "40817810802000000008/044525104",
            "documentId": "1cf95c4f-e794-4407-bac4-0829f19bd2be",
            "Content": {
                "Act": {
                    "number": "3",
                    "basedOn": "Основание платежа",
                    "comment": "Комментарий",
                    "date": "2021-05-06",
                    "totalAmount": "12345",
                    "totalNds": "1",
                    "Positions": [
                        {
                            "positionName": "Название товара или услуги",
                            "unitCode": "шт.",
                            "ndsKind": "nds_0",
                            "price": "12345.00",
                            "quantity": "12345",
                            "totalAmount": "12345",
                            "totalNds": "1"
                        }
                    ]
                }
            },
            "SecondSide": {
                "accountId": "40817810802000000008/044525104",
                "legalAddress": "197183, г. Санкт-Петербург, ул. Сестрорецкая, д. 8",
                "kpp": "668101001",
                "bankName": "ООО \"БАНК ТОЧКА\"",
                "bankCorrAccount": "30101810745374525104",
                "taxCode": "660000000000",
                "type": "company",
                "secondSideName": "ООО \"ГОС-АЛЬЯНС\""
            }
        }
    })
    headers = {
        'Authorization': 'Bearer <token>',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    main()
