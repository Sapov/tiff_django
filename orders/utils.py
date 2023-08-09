import os
import zipfile
from datetime import date
import shutil
import subprocess
from pathlib import Path

LOCAL_PATH_YADISK = os.getenv('LOCAL_PATH_YADISK')


class Utils:
    organizations = 'Style_N'
    path_save = f'{organizations}/{date.today()}'

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
    def set_dir_media():
        '''выбираем дирикторию media'''
        curent_path = os.getcwd()
        if curent_path[-5:] != 'media':
            os.chdir('media')  # перейти в директорию

    @staticmethod
    def path_for_yadisk(organizations, id_order):
        path_save = f'{organizations}/{date.today()}'
        # --------------------------Work in Yandex Disk--------------------------------#
        path_for_yandex_disk = f'{path_save}/{id_order}'  # Путь на яндекс диске для публикации
        return path_for_yandex_disk

        # path_for_yadisk = Utils.path_for_yadisk()


class Yadisk:

    path = Utils.path_save

    @classmethod
    def create_folder(cls, path=path):
        '''Добавляем фолдер дата
        Директория должна быть всегда уникальной к примеру точная дата мин/сек
        '''
        if os.path.exists(f"{LOCAL_PATH_YADISK}{path}"):
            print('Директория уже создана')
        else:
            os.mkdir(f'{LOCAL_PATH_YADISK}{path}')

    @classmethod
    def add_yadisk_locate(cls, path=path):
        """закидываем файлы на yadisk локально на ubuntu"""
        Path.cwd()  # Идем в текущий каталог
        lst_files = os.listdir()  # read name files from folder
        for i in lst_files:
            if i.endswith("txt") or i.endswith("zip"):
                print(f'Копирую {i} в {LOCAL_PATH_YADISK}{path}')
                shutil.move(i, f'{LOCAL_PATH_YADISK}{path}')

    @classmethod
    def add_link_from_folder_yadisk(cls, path=path):
        print(f'Публикую папку: {LOCAL_PATH_YADISK}{path}')
        ya_link = subprocess.check_output(["yandex-disk", "publish", f'{LOCAL_PATH_YADISK}{path}'])
        ya_link = str(ya_link)
        ya_link = ya_link.lstrip("b'")
        print(ya_link)
        ya_link = ya_link.rstrip("\n'")
        print(f'Ссылка на яндекс диск {ya_link}')
        return ya_link
