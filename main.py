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


# def get_status_invoice():
#     url = f'https://enter.tochka.com/uapi/invoice/v1.0/bills/301576470/b20791fa-f119-45e2-a34f-1b307e2b9279/payment-status'
#
#     payload = ""
#     headers = {'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
#                }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#
#     print(response.text)
#
#
# get_status_invoice()
