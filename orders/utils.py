import os
import zipfile
from datetime import date


class Utils:
    @staticmethod
    def arhvive(list_files: list, id_order: str) -> None:  # add tif to ZIP file
        '''Архивируем заказ'''
        if os.path.isfile(f'Order_№_{id_order}_{date.today()}.zip'):
            print('Файл уже существует, архивация пропущена')
        else:
            print("Архивируем файлы:", *list_files)
            for name in list_files:
                arh_name = f'Order_№_{id_order}_{date.today()}.zip'
                new_arh = zipfile.ZipFile(arh_name, "a")
                new_arh.write(name, compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()

    @staticmethod
    def set_dir():
        '''выбираем дирикторию media'''
        curent_path = os.getcwd()
        if curent_path[-5:] != 'media':
            os.chdir('media')  # перейти в директорию
