import os
import zipfile
from datetime import date
import shutil
import subprocess
from pathlib import Path

from django.core.mail import send_mail

LOCAL_PATH_YADISK = os.getenv('LOCAL_PATH_YADISK')


class Utils:
    organizations = 'Style_N'
    path_save = f'{organizations}/{date.today()}'

    @staticmethod
    def arhvive(list_files: list, id_order: str) -> str:  # add tif to ZIP file
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
        return f'Order_№_{id_order}_{date.today()}.zip'

    @staticmethod
    def set_dir_media():
        '''выбираем дирeкторию media'''
        print(f' Мы до  выбора директории {os.getcwd()}')
        print(f'Смотрим переменную __file__{__file__}')
        curent_path = os.getcwd()
        if curent_path[-5:] != 'media':
            os.chdir(
                f'media/image/{date.today()}')  # перейти в директорию дата должна браться из параметра Order.created
        print(f' Мы Выбрали {os.getcwd()}')

    @staticmethod
    def path_for_yadisk(organizations, id_order):
        path_save = f'{organizations}/{date.today()}'
        # --------------------------Work in Yandex Disk--------------------------------#
        path_for_yandex_disk = f'{path_save}/{id_order}'  # Путь на яндекс диске для публикации
        return path_for_yandex_disk

    @staticmethod
    def send_mail_order(body_mail):
        ''' принимаем ссылку на яд и текст шаблон письма'''
        send_mail('Новый заказ от REDS',
                  'заказ',
                  'django.rpk@mail.ru',
                  ['rpk.reds@ya.ru'],
                  fail_silently=False,
                  html_message=body_mail)

    def goto_media(foo):
        ''' переходим в паапку media/image{data}  и обратно'''

        def wrapper(*args, **kwargs):
            print(f'[INFO] перед работой мы тут:{os.getcwd()}')
            curent_path = os.getcwd()
            # data_file = Product.objects.get(id=id_order)
            if curent_path[-5:] != 'media':
                os.chdir(
                    f'media/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
            print(f'[INFO] Мы Выбрали {os.getcwd()}')
            res = foo(*args, **kwargs)
            os.chdir(curent_path)  # перейти обратно
            print(f'[INFO] Возвращаемся обратно {os.getcwd()}')
            return res

        return wrapper

    # @staticmethod
    # @goto_media
    # def create_text_file(id_order):
    #     ''' Создаем файл с харaктерисиками файла для печати '''
    #
    #     all_products_in_order = OrderItem.objects.filter(order=id_order, is_active=True)
    #     text_file_name = f'Order_№{id_order}_for_print_{date.today()}.txt'
    #     with open(text_file_name, "w") as text_file:
    #         text_file.write(f'{"*" * 5}   Заказ № {id_order}   {"*" * 5}\n\n')
    #         for item in all_products_in_order:
    #             file = Product.objects.get(id=item.product.id)
    #             file_name = f'Имя файла: {str(file.images)[str(file.images).rindex("/") + 1:]}'  # обрезаем пути оставляем только имя файла
    #             material_txt = f'Материал для печати: {file.material}'
    #             quantity_print = f'Количество: {file.quantity} шт.'
    #             length_width = f'Ширина: {file.width} см\nДлина: {file.length} см\nРазрешение: {file.resolution} dpi'
    #             color_model = f'Цветовая модель: {file.color_model}'
    #             size = f'Размер: {file.size} Мб'
    #             square = f'Площадь: {(file.length * file.width) / 10000} м2'
    #             finish_work_rec_file = f'Финишная обработка: {file.FinishWork}'
    #             fields = f'Поля: {file.Fields}'
    #
    #             text_file.write(
    #                 f'{file_name}\n{material_txt}\n{quantity_print}\n{length_width}\n{square}\n{color_model}\n{size}\n{fields}\n{finish_work_rec_file}\n'
    #             )
    #             text_file.write("-" * 40 + "\n")
    #
    #     return text_file_name


class Yadisk:
    path = Utils.path_save


    def goto_media(foo):
        ''' переходим в паапку media/image{data}  и обратно'''

        def wrapper(*args, **kwargs):
            print(f'[INFO] перед работой мы тут:{os.getcwd()}')
            curent_path = os.getcwd()
            # data_file = Product.objects.get(id=id_order)
            if curent_path[-5:] != 'media':
                os.chdir(
                    f'media/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
            print(f'[INFO] Мы Выбрали {os.getcwd()}')
            res = foo(*args, **kwargs)
            os.chdir(curent_path)  # перейти обратно
            print(f'[INFO] Возвращаемся обратно {os.getcwd()}')
            return res

        return wrapper

    @classmethod
    def create_folder(cls, path=path):
        '''Добавляем фолдер дата
        Директория должна быть всегда уникальной к примеру точная дата мин/сек
        '''
        if os.path.exists(f"{LOCAL_PATH_YADISK}{path}"):
            print('Директория уже создана')
        else:
            os.mkdir(f'{LOCAL_PATH_YADISK}{path}')

    @goto_media
    @classmethod
    def add_yadisk_locate(cls, path=path):

        """закидываем файлы на yadisk локально на ubuntu
        Если состояние заказа ставим обратно в ОФОРМЛЕН, а потом ставим в РАБОТЕ, то файл(архив) на
        Я-ДИСКЕ затирается новым"""
        Path.cwd()  # Идем в текущий каталог
        curent_folder = os.getcwd()
        print('Из яндекс функции видим каталог - ', curent_folder)
        lst_files = os.listdir()  # read name files from folder
        for i in lst_files:
            if i.endswith("txt") or i.endswith("zip"):
                print(f'Копирую {i} в {LOCAL_PATH_YADISK}{path}')
                '''Проверяем есть ли файл'''
                os.chdir(f'{LOCAL_PATH_YADISK}{path}')  # перехожу в я-диск # test print('Теперь мы в', os.getcwd())
                if os.path.exists(i):
                    os.remove(i)  # test print(f'На ya Диске есть такой файл {i} удалим его ')
                    # test print('Check', os.listdir())
                    os.chdir(curent_folder)  # test print('переходим обратно') print('Теперь мы в', os.getcwd())

                    shutil.move(i, f'{LOCAL_PATH_YADISK}{path}')
                    # Возвращаемся в корень  print(f'ВОТ ОН КАСТЫЛЬ {__file__[:-16]}')
                    print(f'ВОТ ОН КАСТЫЛЬ {__file__[:-16]}')
                    os.chdir(__file__[:-16])
                else:
                    os.chdir(curent_folder)
                    shutil.move(i, f'{LOCAL_PATH_YADISK}{path}')
                    # Возвращаемся в корень
                    os.chdir(__file__[:-16])

    @classmethod
    def add_link_from_folder_yadisk(cls, path=path):
        print(f'Публикую папку: {LOCAL_PATH_YADISK}{path}')
        ya_link = subprocess.check_output(["yandex-disk", "publish", f'{LOCAL_PATH_YADISK}{path}'])
        ya_link = str(ya_link)
        ya_link = ya_link.lstrip("b'")
        ya_link = ya_link.rstrip(r"\n'")
        print(f'Ссылка на яндекс диск {ya_link}')
        return ya_link
