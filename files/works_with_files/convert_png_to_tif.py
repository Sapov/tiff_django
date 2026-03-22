import os

from PIL import Image


class ConvertToTif:
    '''
    Конвертируем файл PNG в Tif и пересохраняем его в БД а PNG убиваем
    '''

    def __init__(self, image):
        self.new_name = None
        self.image = image

    def __new_name_file(self):
        self.new_name = str(self.image)[:-4] + '.tif'

    def convert_png_to_tif(self):
        Image.MAX_IMAGE_PIXELS = None

        with Image.open(self.image) as img:
            # Конвертировать и сохранить в TIFF
            img.save(self.new_name, format='TIFF', dpi=(72, 72))
            content_type = 'image/tiff'

    def delete_png(self):
        os.remove(self.image)

    def update_bd_product(self):
        new_file = os.path.basename(self.new_name)
        print(new_file)
        self.image = new_file
        self.image.save()
        'banner_orders/2026/03/22/banner_Q8erJ6a.png'

    def run(self):
        self.__new_name_file()
        self.convert_png_to_tif()
        self.delete_png()
        self.update_bd_product()


if __name__ == '__main__':
    im_new = ConvertToTif('/home/sasha/PycharmProjects/tiff_django/media/image/123.png')
    im_new.run()
