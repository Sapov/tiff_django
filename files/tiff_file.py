import os
import shutil
import zipfile
from datetime import date
import PIL
import data
import patoolib
from PIL import Image as Image_pil, ImageOps
from mysite import settings

import logging

logger = logging.getLogger(__name__)


def check_tiff(file_name: str):
    '''
    :param file_name: принимает имя файла
    :return: возвращает кортеж (длина ширина (см) и разрешение файла (dpi)
    '''

    try:
        Image_pil.MAX_IMAGE_PIXELS = None
        with Image_pil.open(file_name) as img:
            width, length = img.size
            resolution = round(img.info['dpi'][0], 0)
            width = round(2.54 * width / resolution, 0)
            length = round(2.54 * length / resolution, 0)

    except PIL.UnidentifiedImageError:

        return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
Решение: Photoshop / слои / выполнить сведение''')

    return width, length, resolution


class Calculation:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.resolution = None
        self.price = None

    def perimert(self):
        return (self.width + self.length) * 2 / 100  # / 100 приводим к метрам

    def price(self, quantity, material_price):
        price = round(self.width / 100 * self.length / 100 * quantity * material_price)
        # finishka = Calculation(self.width, self.length)
        # self.price += finishka.perimert() * self.finishWork_price  # Добавляю стоимость фиишной обработки
        logger.info(price)
        return price


def goto_media(foo):
    ''' переходим в папку media/image{data}  и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[DECORATOR] перед архивацией МЫ тут{os.getcwd()}')
        current_path = os.getcwd()
        os.chdir(
            f'{settings.MEDIA_ROOT}/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
        logger.info(f' [DECORATOR] Мы Выбрали {os.getcwd()}')
        logger.info(f' [DECORATOR] перед архивацией МЫ тут{os.getcwd()}')
        foo(*args, **kwargs)
        os.chdir(current_path)  # перейти обратно

    return wrapper


class WorkWithFile:
    '''Работа с файлом TIFF'''

    def __init__(self, image):
        self.file_name = None  # имя файла
        self.width = None  # Ширина файла
        self.length = None  # Длина файла
        self.resolution = None  # Разрешение файла
        self.finish_work = None  # финишная обработка
        self.fields = None  # Поля материала
        self.image = image  # Файл

    def price_calculation(self, quantity, material_price):
        '''Расчитываем прайсовую стоимость печати'''
        return round(self.width / 100 * self.length / 100 * quantity * material_price)

    @classmethod
    @goto_media
    def resize_image(cls, file_name: str, new_dpi: int):
        '''
        :param file_name: имя файла для ресайза
        :param new_dpi: новое разрешение ресайза
        :return:
        '''
        if new_dpi <= 0:
            return print("Нельзя устанавливать отрицательное разрешение или  0")
        try:
            Image_pil.MAX_IMAGE_PIXELS = None
            with Image_pil.open(file_name) as img:
                logger.info(img)
                width_px, length_px = img.size
                logger.info(f'{width_px}, {length_px}')
                resolution = round(img.info['dpi'][0], 0)
                logger.info(f'resolution:{resolution}')
                persent_resize = float(new_dpi / resolution)
                logger.info(f'persent_resize {persent_resize}')
                width_new_px = round(float(persent_resize * width_px), 0)
                length_new_px = round((width_new_px / width_px) * length_px, 0)
                print('width_new_px', width_new_px, 'length_new_px', length_new_px)
                img = img.resize((int(width_new_px), int(length_new_px)))
                logger.info(img)
                img.save('new_file.tif', compression='tiff_lzw',
                         dpi=(new_dpi, new_dpi))  # f'{file_name}',  dpi=(new_dpi, new_dpi)
                logger.info(f' МЫ тут{os.getcwd()}')
            logger.info(f'[INFO] Изменил размер файла {file_name} c {resolution} dpi на {new_dpi} dpi\n')
            os.remove(str(file_name))
            logger.info(f'[INFO] Deleting old file  {file_name} ')

            os.rename('new_file.tif', str(file_name))
            logger.info(f'[INFO] COPY new_file.tif {file_name} ')

        except PIL.UnidentifiedImageError:
            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')

    def compress_image(self, resolution):
        try:
            Image_pil.MAX_IMAGE_PIXELS = None
            with Image_pil.open(self.image) as img:
                width_px, length_px = img.size
                img.save(self.image, compression='tiff_lzw', dpi=(resolution, resolution), tiffinfo={317: 2,
                                                                                                     278: 1})  # , dpi=(new_dpi, new_dpi))  # f'{file_name}',  dpi=(new_dpi, new_dpi)
            logger.info(f'COMPRESS {self.image}')

        except PIL.UnidentifiedImageError:
            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')

    def check_resolution(self, resolution_print):
        '''
        Проверяем разрешения и уменьшаем в соответствии со стандартом'''
        logger.info(f'[INFO] это разрешение будем сравнивать {resolution_print}')
        if self.resolution > resolution_print:
            logger.info("[INFO] Разрешение больше необходимого Уменьшаем!!")
            self.resize_image(self.image, resolution_print)
        elif self.resolution == resolution_print:
            logger.info('[INFO] Разрешение соответствует требованиям')
        else:
            logger.info("[INFO] Низкое разрешение не соответствует требованиям")

    def check_tiff(self):
        '''
        :param self.image принимает имя файла
        :return: возращает кортеж (длина, ширина (см) и разрешение файла (dpi)
        '''

        try:
            Image_pil.MAX_IMAGE_PIXELS = None
            with Image_pil.open(self.image) as img:
                width, length = img.size
                self.resolution = round(img.info['dpi'][0], 0)
                self.width = round(2.54 * width / self.resolution, 0)
                self.length = round(2.54 * length / self.resolution, 0)

        except PIL.UnidentifiedImageError:

            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
    Решение: Photoshop / слои / выполнить сведение''')

        return self.width, self.length, self.resolution

    def perimetr(self):  # написать тесты на /0
        return (self.width + self.length) * 2 / 100  # / 100 приводим к метрам

    def finish_wokrs(self, finish_work_price):
        return self.perimetr() * finish_work_price  # Добавляю стоимость финишной обработки

    def color_mode(self) -> str:
        Image_pil.MAX_IMAGE_PIXELS = None

        try:
            with Image_pil.open(self.image) as img:
                mode = img.mode
                if mode == 'CMYK':

                    return mode
                else:
                    logger.info("Цветовая модель не соответствует требованиям, нужно перевести в CMYK")
                    return mode
        except PIL.UnidentifiedImageError:
            logger.info('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')

            return mode

    def number_of_pieces(self, file_name_in_list) -> int:
        '''ищем количество в имени файла указываеться после шт не покрыта тестами'''
        file_name_in_list = file_name_in_list.lower()
        if 'шт' in file_name_in_list:
            quantity_in_name_file = file_name_in_list[:file_name_in_list.find('шт')]
            num = ""
            for i in range(file_name_in_list.find('шт') - 1, -1, -1):
                # print(file_name[i])
                if file_name_in_list[i].isdigit():
                    num += str(file_name_in_list[i])
                    num = num[::-1]
            return int(num)
        else:
            return 1

    def size_file(self, file_name) -> float:
        # Размер в МБ
        file_stat = os.stat(file_name)
        return round(file_stat.st_size / (1024 * 1024), 2)

    def calculation(self, width, length, material: str) -> float:
        if self.type_print == 'Широкоформатная печать':
            price_material = data.propertis_material_sirka[self.material][0]
            return round(width * length * price_material, 2)
        elif self.type_print == 'Интерьерная печать':
            price_material = data.propertis_material_interierka[self.material][0]
            return round(width * length * price_material, 2)

        elif self.type_print == 'УФ-Печать':
            price_material = data.propertis_material_UV[self.material][0]
            return round(width * length * price_material, 2)

    # запись в текстовый файл
    def rec_to_file(self):
        print(CheckImage.__dict__)
        text_file_name = f'{self.material}_for_print_{date.today()}.txt'
        itog = 0

        with open(text_file_name, "w") as file:
            file.write(f'{"#" * 5}   {self.type_print}   {"#" * 5}\n\n')
            for i in range(len(self.lst_tif)):
                w_l_dpi = self.check_tiff(self.lst_tif[i])
                assert type(self.check_tiff(self.lst_tif[i])) == tuple, 'Ожидаем кортеж'
                P = self.perimetr()  # периметр файла
                logger.info(self.fields)

                file_name = f'File # {i + 1}: {self.lst_tif[i]}'
                self.material_txt = f'Материал для печати: {self.material}'
                quantity = int(self.number_of_pieces(self.lst_tif[i]))
                quantity_print = f'Количество: {quantity} шт.'
                length_width = f'Ширина: {w_l_dpi[0]} см\nДлина: {w_l_dpi[1]} см\nРазрешение: {w_l_dpi[2]} dpi'
                color_model = f'Цветовая модель: {self.color_mode(self.lst_tif[i])}'
                size = f'Размер: {self.size_file(self.lst_tif[i])} Мб'
                price_one = self.calculation(w_l_dpi[0] / 100, w_l_dpi[1] / 100, self.material)
                if self.finish_work:
                    f_W = round(data.finishka[self.finish_work][0] * P, 2)
                    finish_work_rec_file = f'Финишная обработка: {self.finish_work} - {f_W} руб.'
                    price_one = price_one + f_W
                else:
                    finish_work_rec_file = f'Финишная обработка: НЕТ'
                square_unit = (w_l_dpi[0] * w_l_dpi[
                    1]) / 10000  # площадь печати одной штуки (см приводим к метрам  / 10 000
                square = f'Площадь печати {round(square_unit * quantity, 2)} м2'  # вся площадь печати
                price = price_one * quantity
                price_print = f'Стоимость: {price_one * quantity} руб.\n '
                itog = itog + price

                file.write(
                    f'{file_name}\n{self.material_txt}\n{quantity_print}\n{length_width}\n{square}\n{color_model}\n{size}\n{self.fields}\n{finish_work_rec_file}\n{price_print}\n'
                )
                file.write("-" * 40 + "\n")

            file.write(f'Итого: {round(itog, 2)} руб.\n')
            logger.info(f'Итого стоимость печати: {round(itog, 2)} руб.')
            return text_file_name


class WorkZip:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def print(name):
        print(os.path.isfile(f'upload_arhive/{name}'))  # True
        print(f'FILE NAME {name}')  # True

    @staticmethod
    def unzip(name):
        print("В начале пути Я", os.getcwd())
        curent_folder = os.getcwd()  # текущая директория
        os.chdir(f'media/upload_arhive')  # перехожу в media/upload_arhive

        print("где я", os.getcwd())
        print('UNZIP files', name)
        patoolib.extract_archive(str(name), outdir="unzip")
        os.chdir(curent_folder)  # перехожу обратно
        print("Теперь я", os.getcwd())

    @classmethod
    def unzip_files(cls):
        os.chdir(f'media/upload_arhive/unzip')
        lst_files = os.listdir()
        print(lst_files)
        return lst_files

    @staticmethod
    def add_files_in_product(request, lst_files):
        os.chdir('unzip')  # перехожу в
        for i in lst_files():
            print(i)
            # Product.objects.create(Contractor=request.user, images=i)


class Image:
    '''Работа с загруженным файлом'''

    def __init__(self, image):
        self.image = image
        self.length = None
        self.width = None
        self.resolution = None

    def dimensions(self):
        '''
        :param self.image принимает имя файла
        :return: возращает кортеж (длина, ширина (см) и разрешение файла (dpi)
        '''

        try:
            Image_pil.MAX_IMAGE_PIXELS = None
            with Image_pil.open(self.image) as img:
                width, length = img.size
                self.resolution = round(img.info['dpi'][0], 0)
                self.width = round(2.54 * width / self.resolution, 0)
                self.length = round(2.54 * length / self.resolution, 0)

        except PIL.UnidentifiedImageError:

            return print('''!!! -- Это ошибка: Не сведенный файл Tiff --- !!!
    Решение: Photoshop / слои / выполнить сведение''')

        return self.width, self.length, self.resolution


class Calculator(Image):
    ''' Класс умеет рассчитывать стоимость печати '''

    def __init__(self, image, role: str, material, finishing, quantity: int):
        super().__init__(image)
        self.quantity = quantity
        self.value_finishing_price = None
        self.finishing = finishing
        self.material = material
        self.role = role
        self.value_material_price = None

    def __print_calculator(self):
        '''Расчитываем прайсовую стоимость печати'''
        return round(self.width / 100 * self.length / 100 * self.value_material_price)

    def __finishing_calculator(self):
        ''' Считаем стоимость финишной обработки'''
        return (self.width + self.length) * 2 / 100 * self.value_finishing_price  # / 100 приводим к метрам

    def __change_role_user(self):
        # проверяем роль пользователя и выбираем стоимость ему соответствующую
        if self.role == "CUSTOMER_RETAIL":
            self.value_material_price = self.material.price_customer_retail
            self.value_finishing_price = self.finishing.price_customer_retail
            print('Считаем по цене', self.value_material_price, 'AND', self.value_finishing_price)
        elif self.role == "CUSTOMER_AGENCY":
            self.value_material_price = self.material.price
            self.finishing = self.finishing.price
        else:
            # Иначе считаем как по CUSTOMER_RETAIL
            self.value_material_price = self.material.price_customer_retail
            self.value_finishing_price = self.finishing.price_customer_retail

    def calculate(self):
        self.__change_role_user()
        return (self.__print_calculator() + self.__finishing_calculator()) * self.quantity

    def calculate_cost(self):
        # СЕБЕСТОИМОСТЬ
        self.value_material_price = self.material.price_contractor
        self.finishing = self.finishing.price_contractor
        return (self.__print_calculator() + self.__finishing_calculator()) * self.quantity
