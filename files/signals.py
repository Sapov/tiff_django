import os
import zipfile
import data
from datetime import date
from tqdm import tqdm

import PIL
from PIL import Image, ImageOps

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Product


def check_tiff(file_name: str):
    '''
    :param file_name: принимает имя файла
    :return: возращает кортеж (длина ширина (см) и разрешение файла (dpi)
    '''

    try:
        Image.MAX_IMAGE_PIXELS = None
        with Image.open(file_name) as img:
            width, length = img.size
            resolution = round(img.info['dpi'][0], 0)
            width = round(2.54 * width / resolution, 0)
            length = round(2.54 * length / resolution, 0)

    except PIL.UnidentifiedImageError:

        return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
Решение: Photoshop / слои / выполнить сведение''')

    return width, length, resolution

def arh(list_files: list, material_name: str) -> None:  # add tif to ZIP file
    if os.path.isfile(f'{material_name}_{date.today()}.zip'):
        print('Файл уже существует, архивация пропущена')
    else:
        print("Архивируем файлы:", *list_files)
        for name in tqdm(list_files):
            arh_name = f'{material_name}_{date.today()}.zip'
            new_arh = zipfile.ZipFile(arh_name, "a")
            new_arh.write(name, compress_type=zipfile.ZIP_DEFLATED)
            new_arh.close()