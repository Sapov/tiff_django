import PIL
from PIL import Image, ImageOps


def check_tiff(file_name: str):
    '''
    :param file_name: принимает имя файла
    :return: возвращает кортеж (длина ширина (см) и разрешение файла (dpi)
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


class Calculation:
    def __init__(self, width, length):
        # self.price = None
        # self.perimetr = None
        # self.quantity = quantity
        # self.material = material
        # self.resolution = None
        self.width = width
        self.length = length
        # self.images = images
        # self.finishWork_price = finishWork_price

    def size_images(self):
        width, length, resolution = check_tiff(self.images)  # Читаем размеры из Tiff
        self.width = width
        self.length = length
        self.resolution = resolution
        print('размеры', self.width, self.length)

    def price(self):
        self.price = round(self.width / 100 * self.length / 100 * self.quantity * self.material.price)
        print('PRICE', self.price)
        return self

    def perimert(self):
        perimetr = (self.width + self.length) * 2 / 100  # / 100 приводим к метрам
        return perimetr

    def price_finishka(self):
        self.price += self.perimetr * self.finishWork_price
        return self.price
