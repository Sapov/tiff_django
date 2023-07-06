import os

import PIL
from PIL import Image, ImageOps

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Product
# from .tiff_file import thumbnail


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


# @receiver(post_save, sender=Product)
# def post_save_product(**kwargs):
#     instance = kwargs['instance']
#     # print('Если возможно делаем из файла превьюху')
#     # print(instance)
#     print(f'Загрузили файл: {instance.images}')
#     # os.chdir('/media/image/14_03_23')
#     print(check_tiff(instance.images))
#     print(instance.length)
#     instance.width = check_tiff(instance.images)[0]
#     instance.save(force_update=True)
#     print(instance.width)



    # thumbnail(instance.images)
