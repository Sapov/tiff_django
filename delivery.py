import json
import os
import uuid
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class YandexDelivery:
    TOKEN_YANDEX_DELIVERY = os.getenv('TOKEN_YANDEX_DELIVERY')
    url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/offers/calculate'
    headers = {'Accept-Language': 'ru',
               'Authorization': 'Bearer ' + TOKEN_YANDEX_DELIVERY}

    def __init__(self): pass

    def offer_calculate(self):
        data = {
            "items": [
                {
                    "size": {
                        "length": 0.2,
                        "width": 0.2,
                        "height": 0.3
                    },
                    "weight": 2.105,
                    "quantity": 1,
                    "pickup_point": 1,
                    "dropoff_point": 2
                }
            ],
            "route_points": [
                {
                    "id": 1,
                    "coordinates": [51.759647, 39.180270],
                    "fullname": "Московский проспект,197"
                },
                {
                    "id": 2,
                    "coordinates": [51.711656, 39.163233],
                    "fullname": "улица 60-й Армии, 27"
                }
            ],
            "requirements": {
                "taxi_classes": [
                    "cargo"
                ],
                "cargo_type": "lcv_m",
                "cargo_loaders": 1,
                "pro_courier": False,
                "cargo_options": ["auto_courier"],
                "skip_door_to_door": False,
                "due": "2024-07-28T21:30:00+00:00"
            }
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        print(response)
        print(response.status_code)

        print(response.text)

    def create_delivery_order(self):
        data = {
            "shipping_document": "string",
            "items": [
                {
                    "extra_id": "БП-208",
                    "pickup_point": 1,
                    "dropoff_point": 2,
                    "droppof_point": 0,
                    "title": "Плюмбус",
                    "size": {
                        "length": 0.1,
                        "width": 0.2,
                        "height": 0.3
                    },
                    "weight": 2,
                    "cost_value": "2.00",
                    "cost_currency": "RUB",
                    "quantity": 1,
                    "fiscalization": {
                        "excise": "12.50",
                        "vat_code_str": "vat_none",
                        "supplier_inn": 3664069397,
                        "article": "20ML50OWKY4FC86",
                        "mark": {
                            "kind": "gs1_data_matrix_base64",
                            "code": "444D00000000003741"
                        },
                        "item_type": "product"
                    }
                }
            ],
            "route_points": [
                {
                    "point_id": 6987,
                    "visit_order": 1,
                    "contact": {
                        "name": "Морти",
                        "phone": "+79099999998",
                        "phone_additional_code": "602 17 500",
                        "email": "example@yandex.ru"
                    },
                    "address": {
                        "fullname": "Санкт-Петербург, Большая Монетная улица, 1к1А",
                        "shortname": "Большая Монетная улица, 1к1А",
                        "coordinates": [
                            0
                        ],
                        "country": "Россия",
                        "city": "Санкт-Петербург",
                        "building_name": "БЦ На Большой Монетной",
                        "street": "Большая Монетная улица",
                        "building": "23к1А",
                        "porch": "A",
                        "sfloor": "1",
                        "sflat": "1",
                        "door_code": "169",
                        "door_code_extra": "код на вход во двор #1234, код от апартаментов #4321",
                        "doorbell_name": "Магидович",
                        "comment": "Домофон не работает",
                        "uri": "ymapsbm1://geo?ll=38.805%2C55.084",
                        "description": "Санкт-Петербург, Россия"
                    },
                    "skip_confirmation": False,
                    "leave_under_door": False,
                    "meet_outside": False,
                    "no_door_call": False,
                    "type": "source",
                    "buyout": {
                        "payment_method": "card"
                    },
                    "payment_on_delivery": {
                        "customer": {
                            "inn": 3664069397,
                            "email": "example@yandex.ru",
                            "phone": "79000000000"
                        },
                        "payment_method": "card"
                    },
                    "external_order_id": "100",
                    "external_order_cost": {
                        "value": "100.0",
                        "currency": "RUB",
                        "currency_sign": "₽"
                    },
                    "pickup_code": "893422",
                    "payment_at_point": "cash"
                }
            ],
            "emergency_contact": {
                "name": "Рик",
                "phone": "+79826810246",
                "phone_additional_code": "602 17 500"
            },
            "client_requirements": {
                "taxi_class": "express",
                "cargo_type": "lcv_m",
                "cargo_loaders": 0,
                "cargo_options": [
                    "thermobag"
                ],
                "pro_courier": false
            },
            "callback_properties": {
                "callback_url": "https://www.example.com/"
            },
            "skip_door_to_door": False,
            "skip_client_notify": False,
            "skip_emergency_notify": False,
            "skip_act": False,
            "optional_return": False,
            "due": "2020-01-01T00:00:00+00:00",
            "comment": "Ресторан",
            "referral_source": "bitrix",
            "same_day_data": {
                "delivery_interval": {
                    "from": "2020-01-01T07:00:00+00:00",
                    "to": "2020-01-01T07:00:00+00:00"
                }
            },
            "auto_accept": False,
            "offer_payload": "asjdijasDKL;ahsdfljhlkjhasF;HS;Ldjf;ljloshf",
            "features_context": {}
        }

    # print(uuid.uuid4())


if __name__ == '__main__':
    YandexDelivery().offer_calculate()
