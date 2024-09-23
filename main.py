import os
from dotenv import load_dotenv, find_dotenv

from orders.models import BankInvoices

load_dotenv(find_dotenv())

import requests


# def get_customer_code():
#     url = "https://enter.tochka.com/uapi/open-banking/v1.0/customers"
#     payload = {}
#     headers = {
#         'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     customer_code = response.json()['Data']['Customer'][0]['customerCode']
#     print(response.json())
#     print(customer_code)
#
# get_customer_code()


def get_status_invoice():
    url = f'https://enter.tochka.com/uapi/invoice/v1.0/bills/00825922-fe8e-47ed-a29d-496ed331ad18/payment-status'

    payload = ""
    headers = {'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
               }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


get_status_invoice()
