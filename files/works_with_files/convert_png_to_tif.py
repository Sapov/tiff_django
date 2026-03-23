import os
from PIL import Image
import logging
from mysite import settings


logger = logging.getLogger(__name__)


def goto_media(foo):
    ''' переходим в папку media/image{data}  и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[DECORATOR] перед обработкой файла МЫ тут{os.getcwd()}')
        current_path = os.getcwd()
        os.chdir(
            f'{settings.MEDIA_ROOT}/image/')
        logger.info(f' [DECORATOR] Мы Выбрали {os.getcwd()}')
        logger.info(f' [DECORATOR] перед архивацией МЫ тут{os.getcwd()}')
        foo(*args, **kwargs)
        os.chdir(current_path)  # перейти обратно

    return wrapper


class ConvertToTif:
    '''
    Конвертируем файл PNG в Tif и пересохраняем его в БД а PNG убиваем
    '''

    def __init__(self, image):
        self.new_name = 'temp.tif'
        self.image = image

        print(f'[пришел type теперь]{type(self.image)}')
        print(f'[пришел]{self.image}')

    def __new_name_file(self):
        self.new_name = str(self.image)[:-4] + '.tif'

    @goto_media
    def convert_png_to_tif(self):

        Image.MAX_IMAGE_PIXELS = None
        with Image.open(self.image) as img:
            try:
                # Конвертировать и сохранить в TIFF
                self.__new_name_file()
                dpi = 96
                img.info['dpi'] = (dpi, dpi)
                print(img.info)

                img.save(self.image,
                         format='TIFF',
                         compression='tiff_lzw',  # LZW компрессия для печати
                         dpi=(dpi, dpi))

                content_type = 'image/tiff'
            except Exception as e:
                print(f'Error {e}')

    def delete_png(self):
        os.remove(str(self.image))

    def run(self):
        self.convert_png_to_tif()
        return self.new_name


if __name__ == '__main__':
    im_new = ConvertToTif('/home/sasha/PycharmProjects/tiff_django/media/image/banner_w5FkKur.tif')
    im_new.run()
