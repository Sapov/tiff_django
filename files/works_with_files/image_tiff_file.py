import os
from datetime import date
from PIL import ImageOps, Image
from math import ceil
import PIL
import logging
from mysite import settings

Image.MAX_IMAGE_PIXELS = None

logger = logging.getLogger(__name__)


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
        width: float Ширина
        length: float Длина
        resolution: float Разрешение
        """
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.image) as img:
                self.width_px, self.length_px = img.size
                self.resolution = int(round(img.info['dpi'][0], 0))
                self.width = round(2.54 * self.width_px / self.resolution, 0) / 100
                self.length = round(2.54 * self.length_px / self.resolution, 0) / 100
                logger.info(f'[SIZE File] :{self.width} m X {self.length} m')
                logger.info(f'[SIZE File PIXELS] :width: {self.width_px} px, length: {self.length_px} px')
                logger.info(f'[RESOLUTION] : {self.resolution} px')

        except PIL.UnidentifiedImageError:

            return '''!!! -- Это ошибка: Не сведенный файл Tiff --- !!!
    Решение: Photoshop / слои / выполнить сведение'''

        return self.width, self.length, self.resolution

    def resolution_reduction(self, new_resolution: int):
        '''Уменьшаем избыточное разрешение для печати'''
        self.dimensions()
        multiplier_width = self.width_px / self.resolution
        multiplier_length = self.length_px / self.resolution
        new_width_px = int(multiplier_width * new_resolution)
        new_length_px = int(multiplier_length * new_resolution)
        self.width = round((2.54 * multiplier_width) / 100, 2)
        self.length = ceil(2.54 * multiplier_length) / 100
        print(f'[RESIZE File] New Size:{self.width} m X {self.length} m')
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.image) as file:
                file = file.resize(size=(new_width_px, new_length_px))
                file.save(self.image, compression='tiff_lzw',
                          dpi=(new_resolution, new_resolution))
                logger.info(f'[Уменьшил разрешение до положенного] {new_resolution}')

        except Exception as Ex:
            print(Ex)



    def draw_outline_image(self):
        # Делаем обводку вокруг файла, часто файлы имею много белого  - непонятно как его разрезать
        res = self.dimensions()[2]
        file = Image.open(self.image)
        img_border = ImageOps.expand(file, border=2, fill='black')
        img_border.save(self.image, compression='tiff_lzw', dpi=(res, res))
        logger.info(f'[INFO] Обвел картинку контуром')

    def resize_image(self, new_dpi: int):
        '''
        :param self.image: имя файла для ресайза
        :param new_dpi: новое разрешение ресайза
        :return:
        '''
        if new_dpi <= 0:
            return "Нельзя устанавливать отрицательное разрешение или  0"
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.image) as img:
                width_px, length_px = img.size
                resolution = round(img.info['dpi'][0], 0)
                logger.info(f'[info] Resolution: {resolution} dpi')
                persent_resize = float(new_dpi / resolution)
                logger.info(f'persent_resize {persent_resize}')
                width_new_px = round(float(persent_resize * width_px), 0)
                length_new_px = round((width_new_px / width_px) * length_px, 0)
                print(f'[INFO] width_new_px: {width_new_px} px, length_new: {length_new_px} px')
                img = img.resize((int(width_new_px), int(length_new_px)))
                logger.info(img)
                img.save('new_file.tif', compression='tiff_lzw', dpi=(new_dpi, new_dpi))
                logger.info(f' МЫ тут{os.getcwd()}')
            logger.info(f'[INFO] Изменил размер файла {self.image} c {resolution} dpi на {new_dpi} dpi\n')
            os.remove(str(self.image))
            logger.info(f'[INFO] Deleting old file  {self.image} ')

            os.rename('new_file.tif', str(self.image))
            logger.info(f'[INFO] COPY new_file.tif {self.image} ')

        except PIL.UnidentifiedImageError:
            return print('''!!! -- Это ошибка: Не сведенный файл Tif --- !!!
                Решение: Photoshop / слои / выполнить сведение''')


# Проверяем разрешение файла для печати
# Уменьшаем избыточное разрешение
# обводим контуром изображение для печати

if __name__ == '__main__':
    im_new = ImageFile('/home/sasha/PycharmProjects/tiff_django/media/image/123.png')
