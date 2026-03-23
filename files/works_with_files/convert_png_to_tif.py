import os

from PIL import Image


class ConvertToTif:
    '''
    Конвертируем файл PNG в Tif и пересохраняем его в БД а PNG убиваем
    '''

    def __init__(self, image):
        self.new_name = 'temp.tif'
        self.image = image

    def __new_name_file(self):
        self.new_name = str(self.image)[:-4] + '.tif'

    def convert_png_to_tif(self):
        Image.MAX_IMAGE_PIXELS = None

        with Image.open(self.image) as img:
            try:
                # Конвертировать и сохранить в TIFF
                dpi = 72
                # img.info['dpi'] = (dpi, dpi)
                print(img.info)

                img.save(self.new_name,
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
        self.__new_name_file()
        # self.delete_png()
        return self.new_name


if __name__ == '__main__':
    im_new = ConvertToTif('/home/sasha/PycharmProjects/tiff_django/media/image/banner.tif')
    im_new.run()
