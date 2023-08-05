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
        self.width = width
        self.length = length

    def perimert(self):
        return (self.width + self.length) * 2 / 100  # / 100 приводим к метрам


class Calc:
    def __init__(self, images, material_price, quantity, finishWork_price):
        self.price = None
        self.quantity = None
        self.finishWork_price = None
        self.images = None
        self.length = None
        self.width = None
        self.material_price = None
        self.images = images
        self.material_price = material_price
        self.quantity = quantity
        self.finishWork_price = finishWork_price

    def price(self):
        self.width, self.length, _ = check_tiff(self.images)  # Читаем размеры из Tiff
        self.price = round(self.width / 100 * self.length / 100 * self.quantity * self.material_price)
        finishka = Calculation(self.width, self.length)
        self.price += finishka.perimert() * self.finishWork_price  # Добавляю стоимость фиишной обработки
        print(self.price)
        return self.price
