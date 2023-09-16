import os
# from os import path

import zipfile
from datetime import date
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.mail import send_mail

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.styles import ParagraphStyle
from .models import OrderItem, Order

import logging
logger = logging.getLogger(__name__)

LOCAL_PATH_YADISK = os.getenv('LOCAL_PATH_YADISK')


class Utils:
    organizations = 'Style_N'
    path_save = f'{organizations}/{date.today()}'

    @staticmethod
    def arhvive(list_files: list, id_order: str) -> str:  # add tif to ZIP file
        '''Архивируем заказ'''
        if os.path.isfile(f'Order_№_{id_order}_{date.today()}.zip'):
            print('Файл уже существует, архивация пропущена')
        else:
            print("Архивируем файлы:", *list_files)
            for name in list_files:
                arh_name = f'Order_№_{id_order}_{date.today()}.zip'
                new_arh = zipfile.ZipFile(arh_name, "a")
                new_arh.write(name, compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()
        return f'Order_№_{id_order}_{date.today()}.zip'

    @staticmethod
    def set_dir_media():
        '''выбираем дирeкторию media'''
        print(f' Мы до  выбора директории {os.getcwd()}')
        print(f'Смотрим переменную __file__{__file__}')
        curent_path = os.getcwd()
        if curent_path[-5:] != 'media':
            os.chdir(
                f'media/image/{date.today()}')  # перейти в директорию дата должна браться из параметра Order.created
        print(f' Мы Выбрали {os.getcwd()}')

    @staticmethod
    def path_for_yadisk(organizations, id_order):
        path_save = f'{organizations}/{date.today()}'
        # --------------------------Work in Yandex Disk--------------------------------#
        path_for_yandex_disk = f'{path_save}/{id_order}'  # Путь на яндекс диске для публикации
        return path_for_yandex_disk

    @staticmethod
    def send_mail_order(body_mail):
        ''' принимаем ссылку на яд и текст шаблон письма'''
        send_mail('Новый заказ от REDS',
                  'заказ',
                  'django.rpk@mail.ru',
                  ['rpk.reds@ya.ru'],
                  fail_silently=False,
                  html_message=body_mail)


def goto_media(foo):
    ''' переходим в папку media/image{data}  и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
        curent_path = os.getcwd()
        # logger.info(f'[INFO DECORATOR] OBJECT: {order_id}')
        # data_file = Product.objects.get(id=self.order_id)
        # logger.info(f'[INFO DECORATOR] OBJECT: {data_file}')
        # logger.info(f'[INFO DECORATOR] CREATED: {data_file.created}')
        # перейти в директорию дата должна браться из параметра Order.created
        os.chdir(
            f'{settings.MEDIA_ROOT}/image/{str(date.today())}')
        logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
        res = foo(*args, **kwargs)
        os.chdir(curent_path)  # перейти обратно
        logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
        return res

    return wrapper




class DrawOrder:
    '''Генерируем счет PDF'''

    fild_bank = [16, 116], [284, 272]  # х началоб х конец у начало у конец
    field_bik = [116, 132], [284, 279]  # BIK
    order_kp = [116, 132], [284, 272]  # order kp #
    self_num = [132, 192], [284, 272]  # self num
    field_inn = [16, 66], [272, 268]  # self INN
    field_kpp = [66, 116], [272, 268]  # self kpp
    field_ip = [16, 116], [256, 268]  # ip
    field_order_ip = [116, 132], [256, 272]  # ip
    field_order_ip1 = [132, 192], [256, 272]  # ip

    fields_position = {'X_START_FIELD_NUMBER': 16, 'X_FINISH_FIELD_NUMBER': 26,
                       'X_START_FIELD_PRODUCT': 26, 'X_FINISH_FIELD_PRODUCT': 118,
                       'X_START_FIELD_QUNTITY': 118, 'X_FINISH_FIELD_QUNTITY': 135,
                       'X_START_ED': 135, 'X_FINISH_FIELD_ED': 145,
                       'X_START_FIELD_PRICE': 145, 'X_FINISH_FIELD_PRICE': 170,
                       'X_START_FIELD_T_PRICE': 170, 'X_FINISH_FIELD_T_PRICE': 192,
                       'Y_START': 205, 'Y_FINISH': 200,
                       }

    def __init__(self, order_id):
        self.font_path = None
        self.order_id = order_id
        self.canvas = Canvas(f'Order_{self.order_id}.pdf', pagesize=A4, )
        curent_order = Order.objects.get(pk=order_id)
        # --------------- order pdf----------
        logging.info(curent_order.organisation_payer, curent_order.organisation_payer.inn)
        self.buyer = (curent_order.organisation_payer.name_ul, curent_order.organisation_payer.inn,
                      curent_order.organisation_payer.address_ur, curent_order.organisation_payer.phone)

    def change_path(self):
        app_path = os.path.realpath(os.path.dirname(__file__))
        self.font_path = os.path.join(app_path, 'fonts/arialmt.ttf')
    def draw_field(self, field):
        self.canvas.grid([field[0][0] * mm, field[0][1] * mm],
                    [field[1][0] * mm, field[1][1] * mm])

    def create_draw_string(self):
        pdfmetrics.registerFont(TTFont('Arial', self.font_path, 'UTF-8'))

        self.canvas.setFont('Arial', 12)
        self.canvas.drawString(17 * mm, 280 * mm, 'ООО "Банк Точка"')
        self.canvas.drawString(117 * mm, 280 * mm, 'БИК')
        self.canvas.drawString(133 * mm, 280 * mm, '044525104')  # bik number
        self.canvas.drawString(117 * mm, 275 * mm, 'Сч. №')  # Order number 1
        self.canvas.drawString(133 * mm, 275 * mm, '30101810745374525104')  # self Order number kor schet
        self.canvas.drawString(17 * mm, 268.5 * mm, 'ИНН    366202910465')  # ИНН
        self.canvas.drawString(67 * mm, 268.5 * mm, 'КПП')  # КПП
        self.canvas.drawString(117 * mm, 268.5 * mm, 'Сч. №')  # Order number 2
        self.canvas.drawString(133 * mm, 268.5 * mm, '40802810108500016162')  # self NUM order
        self.canvas.drawString(17 * mm, 264 * mm, 'ИП Сапов Александр Николаевич')  # ИП

        self.canvas.setFont('Arial', 8)
        self.canvas.drawString(17 * mm, 273 * mm, 'ООО "Банк получателя"')
        self.canvas.drawString(17 * mm, 257 * mm, 'Получатель')

        self.canvas.setFont('Arial', 9)
        self.canvas.drawString(17 * mm, 230 * mm, 'Поставщик')
        self.canvas.setFont('Arial', 12)
        self.canvas.drawString(35 * mm, 230 * mm, 'ИП Сапов Александр Николаевич, ИНН 366202910465, 394066, г. Воронеж,')
        self.canvas.drawString(35 * mm, 225 * mm, 'Московский проспект, дом. № 197, квартира 215, тел. +7-953-119-33-67')
        self.canvas.setFont('Arial', 7)
        self.canvas.drawString(17 * mm, 225 * mm, '(Исполнитель):')

        self.canvas.setFont('Arial', 9)
        self.canvas.drawString(17 * mm, 218 * mm, 'Покупатель')
        self.canvas.setFont('Arial', 12)

        self.canvas.setFont('Arial', 7)
        self.canvas.drawString(17 * mm, 213 * mm, '(Заказчик)')

    def create_dinamic_data(self):
        pdfmetrics.registerFont(TTFont('Arial', self.font_path, 'UTF-8'))

        self.canvas.setFont('Arial', 14)

        self.canvas.drawString(17 * mm, 245 * mm, f'Счет на оплату № {self.order_id} {self.create_data_order()}')
        self.canvas.line(16 * mm, 240 * mm, 193 * mm, 240 * mm)

    def split_string(self ):
        ''' Функция переносит строку по пробелам если строка больше 40 символов'''
        pdfmetrics.registerFont(TTFont('Arial', self.font_path, 'UTF-8'))

        self.canvas.setFont('Arial', 12)
        self.canvas.drawString(35 * mm, 218 * mm, f'{self.buyer[0]} ИНН: {self.buyer[1]} Адрес: {self.buyer[2]}')

    def create_data_order(self):
        st = date.today()
        st = (st.strftime('%Y, %m, %d'))
        calendar = {'01': 'января',
                    '02': 'февраля',
                    '03': 'марта',
                    '04': 'апреля',
                    '05': 'мая',
                    '06': 'июня',
                    '07': 'июля',
                    '08': 'августа',
                    '09': 'сентября',
                    '10': 'октября',
                    '11': 'ноября',
                    '12': 'декабря',
                    }

        string_date = f'от {st[10:]} {calendar[st[6:8]]} {st[:4]} г.'
        return string_date

    def create_header_table(self):

        self.canvas.setFont('Arial', 10)
        self.canvas.grid(
            [self.fields_position['X_START_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_NUMBER'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        self.canvas.grid(
            [self.fields_position['X_FINISH_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        self.canvas.grid(
            [self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm, self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        self.canvas.grid(
            [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        self.canvas.grid(
            [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_PRICE'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        self.canvas.grid(
            [self.fields_position['X_FINISH_FIELD_PRICE'] * mm, self.fields_position['X_FINISH_FIELD_T_PRICE'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])

        self.canvas.drawString(18 * mm, (self.fields_position['Y_FINISH'] + 2) * mm, '№')
        self.canvas.drawString(55 * mm, 202 * mm, 'Товар (Услуга)')
        self.canvas.drawString(120 * mm, 202 * mm, 'Кол-во')
        self.canvas.drawString(137 * mm, 202 * mm, 'Ед.')
        self.canvas.drawString(153 * mm, 202 * mm, 'Цена')
        self.canvas.drawString(177 * mm, 202 * mm, 'Сумма')

    def create_row(self):
        pass

    def create_items_order(self):
        ''' начальная высота заполнения таблицы Y_START = 200  Y_FINISH = 195 '''
        Y_START = 200
        Y_FINISH = 195
        self.canvas.setFont('Arial', 8)
        orders = OrderItem.objects.filter(order=self.order_id)
        TOTAL_PRICE = 0
        ITEM = 0
        for i, v in enumerate(orders):
            interliniag = i * 5
            # --------------------INSERT GRID-----------------------------

            self.canvas.grid(
                [self.fields_position['X_START_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_NUMBER'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])

            self.canvas.grid([self.fields_position['X_FINISH_FIELD_NUMBER'] * mm,
                         self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm],
                        [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            self.canvas.grid([self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm,
                         self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
                        [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            self.canvas.grid(
                [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_ED'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            self.canvas.grid(
                [self.fields_position['X_FINISH_FIELD_ED'] * mm, self.fields_position['X_FINISH_FIELD_PRICE'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])  # price
            self.canvas.grid([self.fields_position['X_FINISH_FIELD_PRICE'] * mm,
                         self.fields_position['X_FINISH_FIELD_T_PRICE'] * mm],
                        [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])  # field sum
            # ----------------------- ADD ITEMS____________________

            # {'X_START_FIELD_NUMBER': 16, 'X_FINISH_FIELD_NUMBER': 26,
            #  'X_START_FIELD_PRODUCT': 26, 'X_FINISH_FIELD_PRODUCT': 118,
            #  'X_START_FIELD_QUNTITY': 118, 'X_FINISH_FIELD_QUNTITY': 135,
            #  'X_START_ED': 135, 'X_FINISH_FIELD_ED': 145,
            #  'X_START_FIELD_PRICE': 145, 'X_FINISH_FIELD_PRICE': 170,
            #  'X_START_FIELD_T_PRICE': 170, 'X_FINISH_FIELD_T_PRICE': 192,
            #  'Y_START': 205, 'Y_FINISH': 200,
            #  }
            VERTIKAL = self.fields_position['Y_FINISH'] - 3 - interliniag
            self.canvas.drawString((self.fields_position['X_START_FIELD_NUMBER'] + 3) * mm,
                              (self.fields_position['Y_FINISH'] - 3 - interliniag) * mm,
                              f'{i + 1}')  # ID

            self.canvas.drawString((self.fields_position['X_FINISH_FIELD_NUMBER'] + 2) * mm, VERTIKAL * mm,
                              f'{v.product.material} {v.product.length}x{v.product.width} см')  # Material Wxl
            self.canvas.drawString((self.fields_position['X_FINISH_FIELD_PRODUCT'] + 9) * mm, VERTIKAL * mm,
                              f'{v.quantity}')  # quantity
            self.canvas.drawString((self.fields_position['X_FINISH_FIELD_QUNTITY'] + 2) * mm, VERTIKAL * mm,
                              f' шт.')  # шт
            self.canvas.drawString((self.fields_position['X_FINISH_FIELD_ED'] + 8) * mm, VERTIKAL * mm,
                              f'{v.price_per_item}')  # price Item
            self.canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] + 10) * mm, VERTIKAL * mm,
                              f'{v.total_price}')  # total price item
            TOTAL_PRICE += v.total_price
            ITEM += i + 1
        # --------------------- TOTAL PRICE-----------------
        self.canvas.setFont('Arial', 12)
        self.canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 10) * mm,
                          f'Итого:              {TOTAL_PRICE}')
        self.canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 15) * mm,
                          f'Без налога (НДС)      -')
        self.canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 20) * mm,
                          f'Всего к оплате:   {TOTAL_PRICE}')
        self.canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 25) * mm,
                          f'Всего наименований,{ITEM}, на сумму {TOTAL_PRICE} руб.')
        self.canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 30) * mm,
                          f'Оплата данного счета означает согласие с публичной офертой площадки')
        self.canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 35) * mm,
                          f'Счет действителен в течении трех дней')
        self.canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 40) * mm,
                          f'Предприниматель___________________________ Сапов А.Н.')

    def add_arhive_in_order(self):
        '''Записываем в таблицу ссылку на pdf счет с файлами'''
        order = Order.objects.get(id=self.order_id)
        logger.info(f'LOAD PDF in table: orders/Order#{self.order_id}.pdf')
        order.order_pdf_file = f'orders/Order#{self.order_id}.pdf'
        order.save()

    def run(self):
        self.draw_field(self.fild_bank)
        self.draw_field(self.field_bik)
        self.draw_field(self.order_kp)
        self.draw_field(self.self_num)
        self.draw_field(self.field_inn)
        self.draw_field(self.field_kpp)
        self.draw_field(self.field_ip)
        self.draw_field(self.field_order_ip)
        self.draw_field(self.field_order_ip1)
        self.create_draw_string()
        self.create_header_table()
        self.split_string()
        self.create_items_order()
        self.create_dinamic_data()
        self.canvas.save()
        self.add_arhive_in_order()
