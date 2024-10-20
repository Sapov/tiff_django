import json
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class WebHook:
    url_bank = 'https://enter.tochka.com/uapi/webhook/v1.0/'
    client_id = os.getenv('TOCHKA_CLIENT_ID')
    url_webhook_bank = url_bank + client_id
    url_webhook = os.getenv('WEBHOOK_URL')
    token = os.getenv('TOCHKA_TOKEN')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"

    }

    def get_webhook(self):
        payload = {}
        headers = self.headers
        response = requests.request("GET", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def create_webhook(self):
        # Создание веб хука
        # для адреса "url": "https://orders.san-cd.ru/orders/web_hook"
        payload = json.dumps({
            "webhooksList": [
                "incomingPayment"
            ],
            "url": self.url_webhook
        })
        headers = self.headers
        print(self.url_webhook_bank)
        print(payload)
        response = requests.request("PUT", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def edit_web_hook(self):
        payload = json.dumps({
            "webhooksList": [
                "incomingPayment"
            ],
            "url": self.url_webhook

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('TOCHKA_TOKEN')}"
        }
        response = requests.request("POST", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def delete_web_hook(self):
        payload = {}
        headers = self.headers
        response = requests.request("DELETE", url=self.url_webhook_bank, headers=headers, data=payload)
        print(response.text)

    def send_web_hook(self):
        payload = json.dumps({
            "webhookType": "incomingPayment"
        })
        headers = self.headers
        response = requests.request("POST", url=self.url_webhook_bank + '/test_send', headers=headers, data=payload)
        print(response.text)


if __name__ == '__main__':
    # WebHook().get_webhook()
    # WebHook().delete_web_hook()
    # WebHook().create_webhook()
    WebHook().send_web_hook()



# import jwt
# from jwt import exceptions
# import json
#
# payload = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJTaWRlUGF5ZXIiOiB7ImJhbmtDb2RlIjogIjAwMDAwMDAwMCIsICJiYW5rTmFtZSI6ICJcdTA0MWVcdTA0MWVcdTA0MWUgXHUwNDExXHUwNDMwXHUwNDNkXHUwNDNhIFx1MDQyMlx1MDQzZVx1MDQ0N1x1MDQzYVx1MDQzMCIsICJiYW5rQ29ycmVzcG9uZGVudEFjY291bnQiOiAiMDAwMDAwMDAwMDAwMDAwMDAwMDAiLCAiYWNjb3VudCI6ICIwMDAwMDAwMDAwMDAwMDAwMDAwMCIsICJuYW1lIjogIlx1MDQxOFx1MDQxZiBcdTA0MjJcdTA0MzVcdTA0NDFcdTA0NDIiLCAiYW1vdW50IjogIjQwLjAiLCAiY3VycmVuY3kiOiAiUlVCIiwgImlubiI6ICIwMDAwMDAwMDAwIiwgImtwcCI6ICIwMDAwMDAwMDAwIn0sICJTaWRlUmVjaXBpZW50IjogeyJiYW5rQ29kZSI6ICIwMDAwMDAwMDAiLCAiYmFua05hbWUiOiAiXHUwNDFlXHUwNDFlXHUwNDFlIFx1MDQxMVx1MDQzMFx1MDQzZFx1MDQzYSBcdTA0MjJcdTA0M2VcdTA0NDdcdTA0M2FcdTA0MzAiLCAiYmFua0NvcnJlc3BvbmRlbnRBY2NvdW50IjogIjAwMDAwMDAwMDAwMDAwMDAwMDAwIiwgImFjY291bnQiOiAiMDAwMDAwMDAwMDAwMDAwMDAwMDAiLCAibmFtZSI6ICJcdTA0MThcdTA0MWYgXHUwNDIyXHUwNDM1XHUwNDQxXHUwNDQyIiwgImFtb3VudCI6ICI0MC4wIiwgImN1cnJlbmN5IjogIlJVQiIsICJpbm4iOiAiMDAwMDAwMDAwMCIsICJrcHAiOiAiMDAwMDAwMDAwMCJ9LCAicHVycG9zZSI6ICJcdTA0MjJcdTA0MzVcdTA0NDFcdTA0NDJcdTA0M2VcdTA0MzJcdTA0M2VcdTA0MzUgXHUwNDNkXHUwNDMwXHUwNDM3XHUwNDNkXHUwNDMwXHUwNDQ3XHUwNDM1XHUwNDNkXHUwNDM4XHUwNDM1IFx1MDQzZlx1MDQzYlx1MDQzMFx1MDQ0Mlx1MDQzNVx1MDQzNlx1MDQzMCIsICJkb2N1bWVudE51bWJlciI6ICIwMDAwMCIsICJwYXltZW50SWQiOiAiMDAwMDAwMDAwMCIsICJkYXRlIjogIjIwMTgtMTAtMDEiLCAid2ViaG9va1R5cGUiOiAiaW5jb21pbmdQYXltZW50IiwgImN1c3RvbWVyQ29kZSI6ICIzMDAxMjMxMjMifQ.j7FCYrHL6pmR7m8TZxtBPBdsHG3uOu6bBl7HZq-VaK_LDj7Lyjb_B0L6zWZjVTRWvyfi6CZ-T-yT8IWzXdN5csoIEiwSuzLeC17oW-9c359Z5AYbL9x4SHSlYd3Q_hPM4DQVxPnPKb_IYpZGDCTovU_wtlAxiBdXQbY3qWEzzDzCuqZNjlVQalu7XipuSt7nNDBuwcDWJAC8Ry0U7UwRH6wboufhL7WcrQgsEn-2ZV--sKzinhUyfyYMw8_cFt9MNX3x_x3Fhu56708MDviu57O5u9t-diWrw2X75QKjnlf-PAamb0idK_8bJ5XbLXymnaBuYgSZSd-HZMHYLWiMHDL-z1OIsLgPKanUPJeKsSlmiVA1VJH2oZVRMv9Pf05O_cbN26d-LIjqn9z_m8XeZ1w0I9sfGP96IfT7xONsTLdbTCiKAJ-he4nzscxpzQc3tYnaeqETTZiyjB1U_chh88bG2n_0tNlQEtRT3j0sPyCWX3qLSFlkp6kKmQkIfeBn'
#
# # Публичный ключ Точки. Может быть получен из https://enter.tochka.com/doc/openapi/static/keys/public
# key_json = '{"kty":"RSA","e":"AQAB","n":"rwm77av7GIttq-JF1itEgLCGEZW_zz16RlUQVYlLbJtyRSu61fCec_rroP6PxjXU2uLzUOaGaLgAPeUZAJrGuVp9nryKgbZceHckdHDYgJd9TsdJ1MYUsXaOb9joN9vmsCscBx1lwSlFQyNQsHUsrjuDk-opf6RCuazRQ9gkoDCX70HV8WBMFoVm-YWQKJHZEaIQxg_DU4gMFyKRkDGKsYKA0POL-UgWA1qkg6nHY5BOMKaqxbc5ky87muWB5nNk4mfmsckyFv9j1gBiXLKekA_y4UwG2o1pbOLpJS3bP_c95rm4M9ZBmGXqfOQhbjz8z-s9C11i-jmOQ2ByohS-ST3E5sqBzIsxxrxyQDTw--bZNhzpbciyYW4GfkkqyeYoOPd_84jPTBDKQXssvj8ZOj2XboS77tvEO1n1WlwUzh8HPCJod5_fEgSXuozpJtOggXBv0C2ps7yXlDZf-7Jar0UYc_NJEHJF-xShlqd6Q3sVL02PhSCM-ibn9DN9BKmD"}'
# key = json.loads(key_json)
# jwk_key = jwt.jwk_from_dict(key)
#
#
# try:
#     # тело вебхука
#     webhook_jwt = jwt.JWT().decode(
#         message=payload,
#         key=jwk_key,
#     )
#     print(webhook_jwt)
#     print(json.dumps(webhook_jwt, indent=4))
# except exceptions.JWTDecodeError:
#     # Неверная подпись, вебхук не от Точки или с ним что-то не так
#     pass
#
#
