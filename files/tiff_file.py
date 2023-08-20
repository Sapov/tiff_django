import os
import zipfile
from datetime import date
import PIL
import data
import patoolib
from PIL import Image as Image_pil, ImageOps
from tqdm import tqdm


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
        print(price)
        return price


# def arh(list_files: list, material_name: str) -> None:  # add tif to ZIP file
#     if os.path.isfile(f'{material_name}_{date.today()}.zip'):
#         print('Файл уже существует, архивация пропущена')
#     else:
#         print("Архивируем файлы:", *list_files)
#         for name in tqdm(list_files):
#             arh_name = f'{material_name}_{date.today()}.zip'
#             new_arh = zipfile.ZipFile(arh_name, "a")
#             new_arh.write(name, compress_type=zipfile.ZIP_DEFLATED)
#             new_arh.close()
#

class WorkWithFile:
    '''Работа с файлом TIFF'''

    def __init__(self, type_print, lst_tif, material):
        self.file_name = None  # имя файла
        self.type_print = type_print  # тип печати
        self.lst_tif = lst_tif  # Список тиф файлов
        self.material = material
        self.width = None  # Ширина файла
        self.length = None  # Длина файла
        self.resolution = None  # Разрешение файла
        self.finish_work = None  # финишная обработка
        self.fields = None  # Поля материала

    def goto_media(foo):
        ''' переходим в паапку media/image{data}  и обратно'''

        def wrapper(*args, **kwargs):
            print(f' перед архивацией МЫ тут{os.getcwd()}')
            curent_path = os.getcwd()
            if curent_path[-5:] != 'media':
                os.chdir(
                    f'media/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
            print(f' Мы Выбрали {os.getcwd()}')
            print(f' перед архивацией МЫ тут{os.getcwd()}')
            foo(*args, **kwargs)
            os.chdir(curent_path)  # перейти обратно

        return wrapper

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
                print(img)
                width_px, length_px = img.size
                print(width_px, length_px)
                resolution = round(img.info['dpi'][0], 0)
                print(resolution)
                persent_resize = float(new_dpi / resolution)
                print('persent_resize', persent_resize)
                width_new_px = round(float(persent_resize * width_px), 0)
                length_new_px = round((width_new_px / width_px) * length_px, 0)
                print('width_new_px', width_new_px, 'length_new_px', length_new_px)
                img = img.resize((int(width_new_px), int(length_new_px)))
                print(img)
                # img.save(f'new{file_name}', dpi=(new_dpi, new_dpi))
                img.save(f'{file_name}', dpi=(new_dpi, new_dpi))
                print(img)
                print(f' МЫ тут{os.getcwd()}')
            print(f'[INFO] Изменил размер файла {file_name} c {resolution} dpi на {new_dpi} dpi\n')

        except PIL.UnidentifiedImageError:
            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')

    @classmethod
    def check_resolution(cls, material, resolution_file, download_file):
        '''
        Проверяем разрешения и уменьшаем в соответствии со стандартом
        :param lst_tif:
        :param material:
        :return:
        '''
        print('это будем сравнивать', material.resolution_print)
        if resolution_file > material.resolution_print:
            print("[INFO] Разрешение больше необходимого Уменьшаем!!")
            cls.resize_image(download_file, material.resolution_print)
        elif resolution_file == material.resolution_print:
            print('[INFO] Разрешение соответствует требованиям')
        else:
            print("[INFO] Низкое разрешение не соответствует требованиям")

    def check_tiff(self, file_name: str):
        '''
        :param file_name: принимает имя файла
        :return: возращает кортеж (длина, ширина (см) и разрешение файла (dpi)
        '''

        try:
            Image_pil.MAX_IMAGE_PIXELS = None
            with Image_pil.open(file_name) as img:
                width, length = img.size
                self.resolution = round(img.info['dpi'][0], 0)
                self.width = round(2.54 * width / self.resolution, 0)
                self.length = round(2.54 * length / self.resolution, 0)

        except PIL.UnidentifiedImageError:

            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
    Решение: Photoshop / слои / выполнить сведение''')

        return self.width, self.length, self.resolution

    def perimetr(self):
        return (self.width + self.length) * 2 / 100

    def color_mode(self, file_name) -> str:
        Image_pil.MAX_IMAGE_PIXELS = None

        try:
            with Image_pil.open(file_name) as img:
                mode = img.mode
                if mode == 'CMYK':

                    return mode
                else:
                    print("Цветовая модель не соответствует требованиям, нужно перевести в CMYK")
                    return mode
        except PIL.UnidentifiedImageError:
            print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')
            return mode

    def number_of_pieces(self, file_name_in_list) -> int:
        '''
        ищем количество в имени файла указываеться после шт
        не покрыта тестами
        '''
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
                print(self.fields)

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
            print(f'Итого стоимость печати: {round(itog, 2)} руб.')
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
