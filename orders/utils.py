import os
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
from .models import OrderItem

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


class Yadisk:
    path = Utils.path_save

    # def goto_media(foo):
    #     ''' переходим в паапку media/image{data}  и обратно'''
    #
    #     def wrapper(*args, **kwargs):
    #         print(f'[INFO] перед работой мы тут:{os.getcwd()}')
    #         curent_path = os.getcwd()
    #         # data_file = Product.objects.get(id=id_order)
    #         if curent_path[-5:] != 'media':
    #             os.chdir(
    #                 f'media/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
    #         print(f'[INFO] Мы Выбрали {os.getcwd()}')
    #         res = foo(*args, **kwargs)
    #         os.chdir(curent_path)  # перейти обратно
    #         print(f'[INFO] Возвращаемся обратно {os.getcwd()}')
    #         return res
    #
    #     return wrapper

    @classmethod
    def create_folder(cls, path=path):
        '''Добавляем фолдер дата
        Директория должна быть всегда уникальной к примеру точная дата мин/сек
        '''
        if os.path.exists(f"{LOCAL_PATH_YADISK}{path}"):
            print('Директория уже создана')
        else:
            os.mkdir(f'{LOCAL_PATH_YADISK}{path}')

    @goto_media
    @classmethod
    def add_yadisk_locate(cls, path=path):

        """закидываем файлы на yadisk локально на ubuntu
        Если состояние заказа ставим обратно в ОФОРМЛЕН, а потом ставим в РАБОТЕ, то файл(архив) на
        Я-ДИСКЕ затирается новым"""
        Path.cwd()  # Идем в текущий каталог
        curent_folder = os.getcwd()
        print('Из яндекс функции видим каталог - ', curent_folder)
        lst_files = os.listdir()  # read name files from folder
        for i in lst_files:
            if i.endswith("txt") or i.endswith("zip"):
                print(f'Копирую {i} в {LOCAL_PATH_YADISK}{path}')
                '''Проверяем есть ли файл'''
                os.chdir(f'{LOCAL_PATH_YADISK}{path}')  # перехожу в я-диск # test print('Теперь мы в', os.getcwd())
                if os.path.exists(i):
                    os.remove(i)  # test print(f'На ya Диске есть такой файл {i} удалим его ')
                    # test print('Check', os.listdir())
                    os.chdir(curent_folder)  # test print('переходим обратно') print('Теперь мы в', os.getcwd())

                    shutil.move(i, f'{LOCAL_PATH_YADISK}{path}')
                    # Возвращаемся в корень  print(f'ВОТ ОН КАСТЫЛЬ {__file__[:-16]}')
                    print(f'ВОТ ОН КАСТЫЛЬ {__file__[:-16]}')
                    os.chdir(__file__[:-16])
                else:
                    os.chdir(curent_folder)
                    shutil.move(i, f'{LOCAL_PATH_YADISK}{path}')
                    # Возвращаемся в корень
                    os.chdir(__file__[:-16])

    @classmethod
    def add_link_from_folder_yadisk(cls, path=path):
        print(f'Публикую папку: {LOCAL_PATH_YADISK}{path}')
        ya_link = subprocess.check_output(["yandex-disk", "publish", f'{LOCAL_PATH_YADISK}{path}'])
        ya_link = str(ya_link)
        ya_link = ya_link.lstrip("b'")
        ya_link = ya_link.rstrip(r"\n'")
        print(f'Ссылка на яндекс диск {ya_link}')
        return ya_link


canvas = Canvas('Order#1.pdf', pagesize=A4, )


class DrawOder:
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
    buyer = 'ООО "Рога да копыта", ИНН 1234567889, КПП 45645633, тел. +7-982-555-55-22'

    fields_position = {'X_START_FIELD_NUMBER': 16, 'X_FINISH_FIELD_NUMBER': 26,
                       'X_START_FIELD_PRODUCT': 26, 'X_FINISH_FIELD_PRODUCT': 118,
                       'X_START_FIELD_QUNTITY': 118, 'X_FINISH_FIELD_QUNTITY': 135,
                       'X_START_ED': 135, 'X_FINISH_FIELD_ED': 145,
                       'X_START_FIELD_PRICE': 145, 'X_FINISH_FIELD_PRICE': 170,
                       'X_START_FIELD_T_PRICE': 170, 'X_FINISH_FIELD_T_PRICE': 192,
                       'Y_START': 205, 'Y_FINISH': 200,
                       }

    def __init__(self, order_id):
        self.order_id = order_id

    @staticmethod
    def draw_field(field):
        canvas.grid([field[0][0] * mm, field[0][1] * mm],
                    [field[1][0] * mm, field[1][1] * mm])

    @staticmethod
    def create_draw_string():
        pdfmetrics.registerFont(TTFont('Arial', 'arialmt.ttf'))
        canvas.setFont('Arial', 12)
        canvas.drawString(17 * mm, 280 * mm, 'ООО "Банк Точка"')
        canvas.drawString(117 * mm, 280 * mm, 'БИК')
        canvas.drawString(133 * mm, 280 * mm, '044525104')  # bik number
        canvas.drawString(117 * mm, 275 * mm, 'Сч. №')  # Order number 1
        canvas.drawString(133 * mm, 275 * mm, '30101810745374525104')  # self Order number kor schet
        canvas.drawString(17 * mm, 268.5 * mm, 'ИНН    366202910465')  # ИНН
        canvas.drawString(67 * mm, 268.5 * mm, 'КПП')  # КПП
        canvas.drawString(117 * mm, 268.5 * mm, 'Сч. №')  # Order number 2
        canvas.drawString(133 * mm, 268.5 * mm, '40802810108500016162')  # self NUM order
        canvas.drawString(17 * mm, 264 * mm, 'ИП Сапов Александр Николаевич')  # ИП

        canvas.setFont('Arial', 8)
        canvas.drawString(17 * mm, 273 * mm, 'ООО "Банк получателя"')
        canvas.drawString(17 * mm, 257 * mm, 'Получатель')

        canvas.setFont('Arial', 9)
        canvas.drawString(17 * mm, 230 * mm, 'Поставщик')
        canvas.setFont('Arial', 12)
        canvas.drawString(35 * mm, 230 * mm, 'ИП Сапов Александр Николаевич, ИНН 366202910465, 394066, г. Воронеж,')
        canvas.drawString(35 * mm, 225 * mm, 'Московский проспект, дом. № 197, квартира 215, тел. +7-953-119-33-67')
        canvas.setFont('Arial', 7)
        canvas.drawString(17 * mm, 225 * mm, '(Исполнитель):')

        canvas.setFont('Arial', 9)
        canvas.drawString(17 * mm, 218 * mm, 'Покупатель')
        canvas.setFont('Arial', 12)

        canvas.setFont('Arial', 7)
        canvas.drawString(17 * mm, 213 * mm, '(Заказчик)')

    def create_dinamic_data(self):
        pdfmetrics.registerFont(TTFont('Arial', 'arialmt.ttf'))
        canvas.setFont('Arial', 14)

        canvas.drawString(17 * mm, 245 * mm, f'Счет на оплату № {self.order_id} {self.create_data_order()}')
        canvas.line(16 * mm, 240 * mm, 193 * mm, 240 * mm)

    def split_string(self, buyer):
        ''' Функция переносит строку по пробелам если строка больше 40 символов'''
        pdfmetrics.registerFont(TTFont('Arial', 'arialmt.ttf'))
        canvas.setFont('Arial', 12)
        n = 40
        if len(buyer) >= n:
            lst = buyer.split()
            len_string = 0
            for i, v in enumerate(lst):
                if len_string <= n:
                    len_string += len(v)
                else:
                    canvas.drawString(35 * mm, 218 * mm, ' '.join(lst[:i]))
                    canvas.drawString(35 * mm, 213 * mm, ' '.join(lst[i:]))
                    break

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

        canvas.setFont('Arial', 10)
        canvas.grid(
            [self.fields_position['X_START_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_NUMBER'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        canvas.grid(
            [self.fields_position['X_FINISH_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        canvas.grid(
            [self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm, self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        canvas.grid(
            [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        canvas.grid(
            [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_PRICE'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])
        canvas.grid(
            [self.fields_position['X_FINISH_FIELD_PRICE'] * mm, self.fields_position['X_FINISH_FIELD_T_PRICE'] * mm],
            [self.fields_position['Y_START'] * mm, self.fields_position['Y_FINISH'] * mm])

        canvas.drawString(18 * mm, (self.fields_position['Y_FINISH'] + 2) * mm, '№')
        canvas.drawString(55 * mm, 202 * mm, 'Товар (Услуга)')
        canvas.drawString(120 * mm, 202 * mm, 'Кол-во')
        canvas.drawString(137 * mm, 202 * mm, 'Ед.')
        canvas.drawString(153 * mm, 202 * mm, 'Цена')
        canvas.drawString(177 * mm, 202 * mm, 'Сумма')

    def create_row(self):
        pass

    def create_items_order(self):
        ''' начальная высота заполнения таблицы Y_START = 200  Y_FINISH = 195 '''
        Y_START = 200
        Y_FINISH = 195
        canvas.setFont('Arial', 8)
        orders = OrderItem.objects.filter(order=self.order_id)
        TOTAL_PRICE = 0
        ITEM = 0
        for i, v in enumerate(orders):
            interliniag = i * 5
            # --------------------INSERT GRID-----------------------------

            canvas.grid(
                [self.fields_position['X_START_FIELD_NUMBER'] * mm, self.fields_position['X_FINISH_FIELD_NUMBER'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])

            canvas.grid([self.fields_position['X_FINISH_FIELD_NUMBER'] * mm,
                         self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm],
                        [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            canvas.grid([self.fields_position['X_FINISH_FIELD_PRODUCT'] * mm,
                         self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm],
                        [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            canvas.grid(
                [self.fields_position['X_FINISH_FIELD_QUNTITY'] * mm, self.fields_position['X_FINISH_FIELD_ED'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])
            canvas.grid(
                [self.fields_position['X_FINISH_FIELD_ED'] * mm, self.fields_position['X_FINISH_FIELD_PRICE'] * mm],
                [(Y_START - interliniag) * mm, (Y_FINISH - interliniag) * mm])  # price
            canvas.grid([self.fields_position['X_FINISH_FIELD_PRICE'] * mm,
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
            canvas.drawString((self.fields_position['X_START_FIELD_NUMBER'] + 3) * mm,
                              (self.fields_position['Y_FINISH'] - 3 - interliniag) * mm,
                              f'{i + 1}')  # ID

            canvas.drawString((self.fields_position['X_FINISH_FIELD_NUMBER'] + 2) * mm, VERTIKAL * mm,
                              f'{v.product.material} {v.product.length}x{v.product.width} см')  # Material Wxl
            canvas.drawString((self.fields_position['X_FINISH_FIELD_PRODUCT'] + 9) * mm, VERTIKAL * mm,
                              f'{v.quantity}')  # quantity
            canvas.drawString((self.fields_position['X_FINISH_FIELD_QUNTITY'] + 2) * mm, VERTIKAL * mm,
                              f' шт.')  # шт
            canvas.drawString((self.fields_position['X_FINISH_FIELD_ED'] + 8) * mm, VERTIKAL * mm,
                              f'{v.price_per_item}')  # price Item
            canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] + 10) * mm, VERTIKAL * mm,
                              f'{v.total_price}')  # total price item
            TOTAL_PRICE += v.total_price
            ITEM += i + 1
        # --------------------- TOTAL PRICE-----------------
        canvas.setFont('Arial', 12)
        canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 10) * mm,
                          f'Итого:              {TOTAL_PRICE}')
        canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 15) * mm,
                          f'Без налога (НДС)      -')
        canvas.drawString((self.fields_position['X_FINISH_FIELD_PRICE'] - 25) * mm, (VERTIKAL - 20) * mm,
                          f'Всего к оплате:   {TOTAL_PRICE}')
        canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 25) * mm,
                          f'Всего наименований,{ITEM}, на сумму {TOTAL_PRICE} руб.')
        canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 30) * mm,
                          f'Оплата данного счета означает согласие с публичной офертой площадки')
        canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 35) * mm,
                          f'Счет действителен в течении трех дней')
        canvas.drawString(self.fields_position['X_START_FIELD_NUMBER'] * mm, (VERTIKAL - 40) * mm,
                          f'Предприниматель___________________________ Сапов А.Н.')

    def run(self):
        self.draw_field(self.fild_bank)
        self.draw_field(DrawOder.field_bik)
        DrawOder.draw_field(DrawOder.order_kp)
        DrawOder.draw_field(DrawOder.self_num)
        DrawOder.draw_field(DrawOder.field_inn)
        DrawOder.draw_field(DrawOder.field_kpp)
        DrawOder.draw_field(DrawOder.field_ip)
        DrawOder.draw_field(DrawOder.field_order_ip)
        DrawOder.draw_field(DrawOder.field_order_ip1)
        DrawOder.create_draw_string()
        self.create_header_table()
        self.split_string(buyer=DrawOder.buyer)
        self.create_items_order()
        self.create_dinamic_data()
        canvas.save()
