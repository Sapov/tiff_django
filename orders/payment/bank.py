import logging
from datetime import datetime, date
import json
import os
import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from dotenv import load_dotenv, find_dotenv
from django.utils import timezone
from mysite import settings
from orders.models import Order, OrderItem, BankInvoices
import logging

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())


def goto_media_orders(foo):
    ''' переходим в папку media/orders и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
        curent_path = os.getcwd()
        os.chdir(
            f'{settings.MEDIA_ROOT}/orders/')
        logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
        res = foo(*args, **kwargs)
        os.chdir(curent_path)  # перейти обратно
        logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
        return res

    return wrapper


class Bank:
    # url = 'https://enter.tochka.com/sandbox/v2/invoice/v1.0/bills'
    url = "https://enter.tochka.com/uapi/invoice/v1.0/bills"

    def __init__(self, order_id: int):
        self.document_id = None
        self.total_amount_order = 0
        self.order_id = order_id
        self.customer_code = None

    def create_invoice(self):
        payer = Order.objects.get(id=self.order_id)

        payload = json.dumps({
            "Data": {
                "accountId": os.getenv('BANK_ACCOUNT_ID'),
                "customerCode": self.customer_code,
                "SecondSide": {
                    "accountId": f'{payer.organisation_payer.bank_account}/{payer.organisation_payer.bik_bank}',
                    "legalAddress": payer.organisation_payer.address,
                    "kpp": payer.organisation_payer.kpp,
                    "bankName": payer.organisation_payer.bank_name,
                    "bankCorrAccount": payer.organisation_payer.bankCorrAccount,
                    "taxCode": payer.organisation_payer.inn,
                    "type": "company",
                    "secondSideName": payer.organisation_payer.name_full
                },
                "Content": {
                    "Invoice": {
                        "Positions": self.__create_list_position(),
                        "date": str(datetime.now().date()),
                        "totalAmount": self.total_amount_order,
                        "totalNds": "0",
                        "number": self.order_id,
                        # "basedOn": "Основание платежа",
                        # "comment": "Комментарий к платежу",
                    }
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        logging.info(f'RESPONSE  {response}')
        self.document_id = response.json()['Data']['documentId']
        logging.info(f'СГЕНЕРИРОВАЛИ СЧЕТ ПОЛУЧИЛИ DOC ID {self.document_id}')

    def __add_base_document_id(self):
        BankInvoices.objects.create(order_id=self.order_id,
                                    document_id=self.document_id)
        logging.info(f'ЗАПИСАЛИ В БАЗУ ID документа')

    def __create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            total_amount = v.price_per_item * v.product.quantity
            new_dict = {
                "positionName": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "unitCode": "шт.",
                "ndsKind": "without_nds",
                "price": v.price_per_item,
                "quantity": v.product.quantity,
                "totalAmount": total_amount,
                "totalNds": 0
            }
            self.total_amount_order += total_amount
            positions.append(new_dict)
        return positions

    @goto_media_orders
    def get_invoice(self):
        url = f"https://enter.tochka.com/uapi/invoice/v1.0/bills/{self.customer_code}/{self.document_id}/file"
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        with open(f'Order_{self.order_id}.pdf', 'wb') as file:
            file.write(response.content)

    def __get_customer_code(self):
        url = "https://enter.tochka.com/uapi/open-banking/v1.0/customers"
        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)
        self.customer_code = response.json()['Data']['Customer'][0]['customerCode']
        logging.info(f'CUSTOMERCODE {self.customer_code}')

    def add_pdf_in_order(self):
        '''Записываем в таблицу ссылку на pdf счет с файлами'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'ADD PDF in order: orders/Order_{self.order_id}.pdf')
        order.order_pdf_file = f'orders/Order_{self.order_id}.pdf'
        order.save()

    def get_status_invoice(self):
        document = BankInvoices.objects.get(order_id=self.order_id)
        customer_code = 301576470
        url = f'https://enter.tochka.com/uapi/invoice/v1.0/bills/{customer_code}/{document.document_id}/payment-status'

        payload = ""
        headers = {'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
                   }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        payment_status = response.json()['Data']['paymentStatus']
        logging.info(f'PAYMENT STATUS {payment_status}')
        document.payment_Status = payment_status
        document.save()

    def set_status_payment(self):
        '''Меняем статус оплаты'''
        'payment_waiting — оплаты счёта ещё не было;'
        'payment_expired — оплата счёта просрочена. '
        'payment_paid — оплата по счёту прошла.'
        pass

    @classmethod
    def check_payment(cls, domain, order_id):
        PeriodicTask.objects.create(
            name=f'Check payment order №{order_id}',
            task='check_payment_order',
            interval=IntervalSchedule.objects.get(every=1, period='hours'),
            # interval=IntervalSchedule.objects.get(every=2, period='minutes'),
            args=json.dumps([order_id, domain]),
            start_time=timezone.now()
        )

    def run(self):
        self.__get_customer_code()
        self.create_invoice()
        self.__add_base_document_id()
        self.get_invoice()
        self.add_pdf_in_order()
# Запустить фоновую проверку оплаты счета


# from aiohttp import web
# import jwt
# from jwt import exceptions
# import json

# Публичный ключ Точки. Может быть получен из https://enter.tochka.com/doc/openapi/static/keys/public
# key_json = '{"kty":"RSA","e":"AQAB","n":"rwm77av7GIttq-JF1itEgLCGEZW_zz16RlUQVYlLbJtyRSu61fCec_rroP6PxjXU2uLzUOaGaLgAPeUZAJrGuVp9nryKgbZceHckdHDYgJd9TsdJ1MYUsXaOb9joN9vmsCscBx1lwSlFQyNQsHUsrjuDk-opf6RCuazRQ9gkoDCX70HV8WBMFoVm-YWQKJHZEaIQxg_DU4gMFyKRkDGKsYKA0POL-UgWA1qkg6nHY5BOMKaqxbc5ky87muWB5nNk4mfmsckyFv9j1gBiXLKekA_y4UwG2o1pbOLpJS3bP_c95rm4M9ZBmGXqfOQhbjz8z-s9C11i-jmOQ2ByohS-ST3E5sqBzIsxxrxyQDTw--bZNhzpbciyYW4GfkkqyeYoOPd_84jPTBDKQXssvj8ZOj2XboS77tvEO1n1WlwUzh8HPCJod5_fEgSXuozpJtOggXBv0C2ps7yXlDZf-7Jar0UYc_NJEHJF-xShlqd6Q3sVL02PhSCM-ibn9DN9BKmD"}'
# key = json.loads(key_json)
# jwk_key = jwt.jwk_from_dict(key)


def webhook_incoming_payment(request):
    payload = request.text()

    try:
        # тело вебхука
        webhook_jwt = jwt.JWT().decode(
            message=payload,
            key=jwk_key,
        )
    except exceptions.JWTDecodeError:
        # Неверная подпись, вебхук не от Точки или с ним что-то не так
        pass

    # return web.Response(status=200)

    # if request.method == 'POST':
    #     Client.objects.create(
    #     first_name=request.POST['FirstName'],
    #     last_name=request.POST['LastName'],
    #     phone=request.POST['Phone1'],
    #     email=request.POST['Email']
   # )
    return HttpResponse(request.body, status=200)