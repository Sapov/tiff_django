# # from PIL import Image, ImageOps
# # img = Image.open('media/image/1.tif')
# # img_border = ImageOps.expand(img, border=2, fill='blue')
# # img_border.save('1_border.tif')
# import math
# from PIL import Image, ImageDraw
#
# RANGE_LUVERS = 30
#
# with Image.open('media/image/1.tif') as img:
#     # image = Image.new('RGB', (90, 90), 'white')
#     draw = ImageDraw.Draw(img)
#     width, length = img.size
#     print(f'{width} px, {length}px')
#
#     resolution = round(img.info['dpi'][0], 0)
#     width = round(2.54 * width / resolution, 0)
#     length = round(2.54 * length / resolution, 0)
#     print(f'{width} cm, {length}cm')
#     print(
#         f'По ширине можно поставить {math.ceil(width / RANGE_LUVERS) + 1 if width / RANGE_LUVERS % 2 == 0 else math.ceil(width / RANGE_LUVERS)}')
#     print(f'По длине можно поставить {math.ceil(length / RANGE_LUVERS)}')
#     # draw.ellipse((0, 0, 90, 90), 'yellow', 'blue')
# #     img.save('draw-smile.jpg')
# '''
# 1. Получить ширину / длину в px = img.size
# 2. Расставить кружки диаметром 8 мм через 30 или меньше см по периметру
# Отступаем 2 см от края и расчитываем кол-во люверсов
# т.к. width - 4 /
#
# '''

import asyncio

import PIL
from PIL import Image, ImageOps
from math import ceil
import aiohttp
from aiohttp import ClientSession

# async def fetch_status(session: ClientSession, url: str) -> int:
#     async with session.get(url) as result:
#         return result.status
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         url = 'https://san-cd.ru'
#         status = await fetch_status(session, url)
#         print(f'Состояние для {url} было равно {status}')
#
img = Image.open('/home/sasha/Загрузки/test_pic/res_50 Dpi.tif')


class ImageFile:
    '''Работа с загруженным файлом
    dimensions - параметры файла
    resolution_reduction - изменение разрешения файла
    '''

    def __init__(self, image):
        self.width_px = None
        self.length_px = None
        self.image = image
        self.length = None
        self.width = None
        self.resolution = None

    def dimensions(self) -> tuple:
        """
        @return:
        width: float
        length: float
        resolution: float
        """
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.image) as img:
                self.width_px, self.length_px = img.size
                print(f'width: {self.width_px} px, length: {self.length_px} px')
                self.resolution = int(round(img.info['dpi'][0], 0))
                print('RESOLUTION', img.info['dpi'])
                self.width = round(2.54 * self.width_px / self.resolution, 0) / 100
                self.length = round(2.54 * self.length_px / self.resolution, 0) / 100
        except PIL.UnidentifiedImageError:

            return '''!!! -- Это ошибка: Не сведенный файл Tiff --- !!!
    Решение: Photoshop / слои / выполнить сведение'''

        return self.width, self.length, self.resolution

    def resolution_reduction(self, new_resolution: int):
        self.dimensions()
        multiplier_width = self.width_px / self.resolution
        multiplier_length = self.length_px / self.resolution
        new_width_px = ceil(multiplier_width * new_resolution)
        new_length_px = ceil(multiplier_length * new_resolution)
        self.width = ceil(2.54 * multiplier_width * new_resolution / new_resolution) / 100
        self.length = ceil(2.54 * multiplier_length) / 100
        print(f'[RESIZE File] New Size:{self.width} m X {self.length} m')
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.image) as file:
                file = file.resize(size=(new_width_px, new_length_px))
                file.save(self.image, compression='tiff_lzw',
                          dpi=(new_resolution, new_resolution))

        except Exception as Ex:
            print(Ex)

    def draw_outline_image(self):
        # Делаем обводку вокруг файла, часто файлы имею много белого  - непонятно как его разрезать
        res = self.dimensions()[2]
        file = Image.open(self.image)
        img_border = ImageOps.expand(file, border=2, fill='black')
        img_border.save(self.image, compression='tiff_lzw', dpi=(res, res))


# im = ImageFile('/home/sasha/Загрузки/test_pic/85x200.tif')
# im.resolution_reduction(40)
im_new = ImageFile('/home/sasha/Загрузки/test_pic/85x200.tif')

ImageFile('/home/sasha/Загрузки/test_pic/85x200.tif').draw_outline_image()
im_new.dimensions()
