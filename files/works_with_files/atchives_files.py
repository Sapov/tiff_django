import hashlib
import os
import shutil
import zipfile
from datetime import datetime, date
import datetime
from PIL import Image, ImageOps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from files.models import Product
from files.works_with_files import image_tiff_file
from orders.models import Order, logger, OrderItem, StatusOrder
from users.tasks import send_message_whatsapp


class UtilsModel:
    def __init__(self, order_id, domain):
        self.order_complete = None
        self.order_list = None
        self.hash_num = None
        self.arhiv_order_path = None
        self.new_str = None
        self.arh_name = None
        self.order_id = order_id
        self.path_arhive = f"{settings.MEDIA_ROOT}/arhive"
        self.domain = domain
        self.confirm_link_to_work = None

    def send_mail_order(self):
        """отправляем письмо с архивом подрядчику"""
        order = Order.objects.get(id=self.order_id)
        data = {
            "data_order_complete": self.order_complete,
            "order_item": self.order_list,
            "order_archive_link": f"http://{self.domain}/media/{str(order.order_arhive)}",
            "confirm_link": self.confirm_link_to_work,
            "order_id": self.order_id,
        }
        html_message = render_to_string("mail/mail_order_for_typografyl.html", data)
        msg = EmailMultiAlternatives(
            subject=f"Новый заказ от REDS № {self.order_id}",
            to=[
                "rpk.reds@ya.ru",
            ],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    def generate_hash(self):
        self.hash_num = hashlib.md5(str(self.order_id).encode()).hexdigest()
        logger.info(f"GENERATE HASH {self.hash_num}TYPE {type(self.hash_num)}")
        return self.hash_num

    def create_list(self):
        """Создаем list с характеристиками файла для печати"""
        current_path = os.getcwd()
        os.chdir(f"{settings.MEDIA_ROOT}/image/")

        all_products_in_order = OrderItem.objects.filter(order=self.order_id, is_active=True)
        order = Order.objects.get(id=self.order_id)
        # это нужно переписать на нормальный алгоритм с учетом выходных
        self.order_complete = order.date_complete - datetime.timedelta(hours=24)  # Типография от дает на сутки раньше

        self.order_list = []
        for item in all_products_in_order:
            file = Product.objects.get(id=item.product.id)
            file_name = f'Имя файла: {str(file.images)[str(file.images).rindex("/") + 1:]}'  # обрезаем пути оставляем только имя файла
            material_txt = f"Материал для печати: {file.material}"
            quantity_print = f"Количество: {file.quantity} шт."
            length_width = f"Ширина: {file.width} м\nДлина: {file.length} м\nРазрешение: {file.resolution} dpi"
            color_model = f"Цветовая модель: {file.color_model}"
            size = f"Размер: {file.size} Мб"
            square = f"Площадь: {int(file.length * file.width)} м2"
            finish_work_rec_file = f"Финишная обработка: {file.FinishWork}"
            comments = f"Комментарии к файлу: {file.comments}"
            self.order_list.append(file_name)
            self.order_list.append(material_txt)
            self.order_list.append(quantity_print)
            self.order_list.append(length_width)
            self.order_list.append(color_model)
            # self.order_list.append(size)
            self.order_list.append(square)
            self.order_list.append(finish_work_rec_file)

            if comments != "Комментарии к файлу: ":
                self.order_list.append(comments)
            self.order_list.append("-" * 40 + "\n")

        logger.info(f"CREATE LIST, {self.order_list}")

        os.chdir(current_path)

    def archive(self):
        current_path = os.getcwd()  # запоминаем где мы
        os.chdir(f"{settings.MEDIA_ROOT}/image/")  # перейти в директорию image
        """Архивируем заказ"""

        if os.path.isfile(f"Order_№_{self.order_id}_{date.today()}.zip"):
            logger.info("Файл уже существует, архивация пропущена")
        else:
            all_products_in_order = OrderItem.objects.filter(
                order=self.order_id, is_active=True
            )
            logger.info(f'[archive]: Архивируем файлы:", {all_products_in_order}')
            for item in all_products_in_order:
                self.arh_name = f"Order_№_{self.order_id}_{date.today()}.zip"
                new_arh = zipfile.ZipFile(self.arh_name, "a")

                new_name_file = self._rename_files(item)
                logger.info(f'[INFO] Обводим картинку контуром')
                file = image_tiff_file.ImageFile(new_name_file)
                file.draw_outline_image()

                new_arh.write(new_name_file, compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()
        os.chdir(current_path)  # перейти обратно
        return self.arh_name

    def _rename_files(self, item) -> str:
        logger.info(f'----------------Формируем имя файла типа | 5_шт_100х200_Баннер_510_грамм_|------------')
        file = Product.objects.get(id=item.product.id)
        new_name_file = (f"{file.quantity}_шт_{float(file.width)}x{float(file.length)}_"
                         f"{'_'.join(str(file.material).split())}_"
                         f"{'_'.join(str(file.FinishWork).split())}_{file.id}{str(file.images)[-4:]}")
        logger.info(f'[new Name FILE] {new_name_file}')
        logger.info(f'file.images: {file.images}')
        logger.info(f'[OLD name FILE] {str(file.images)[str(file.images).rindex("/") + 1:]}')
        old_name = str(file.images)[str(file.images).rindex("/") + 1:]
        shutil.copy(old_name, new_name_file)
        return new_name_file

    def create_folder_server(self):
        """Добавляем фолдер Директория номер заказа"""
        current_path = os.getcwd()
        os.chdir(f"{settings.MEDIA_ROOT}/arhive")  # перейти в директорию orders
        logger.info(f"[INFO DECORATOR] Мы Выбрали: {os.getcwd()}")
        if os.path.exists(f"{settings.MEDIA_ROOT}/arhive/{self.order_id}"):
            logger.info(f"Директория {self.order_id} уже создана")
        else:
            logger.info(f"Создаем Директорию {self.order_id}")
            os.makedirs(str(self.order_id))
        os.chdir(current_path)  # перейти обратно

    def copy_files_in_server(self):
        """закидываем файлы на order локально на ubuntu
        Если состояние заказа ставим обратно в ОФОРМЛЕН, а потом ставим в РАБОТЕ, то файл(архив) на
        ДИСКЕ затирается новым"""
        self.arhiv_order_path = f"{self.path_arhive}/{self.order_id}"
        os.chdir(f"{settings.MEDIA_ROOT}/image/")
        current_folder = os.getcwd()
        logger.info(f"Из copy_files_in_server функции видим каталог - {current_folder}")
        lst_files = os.listdir()  # read name files from folder
        for i in lst_files:
            if i.endswith("txt") or i.endswith("zip"):
                logger.info(f"Копирую {i} в {self.arhiv_order_path}")
                os.chdir(self.arhiv_order_path)  # перехожу в диск
                if os.path.exists(i):
                    os.remove(
                        i
                    )  # test print(f'На ya Диске есть такой файл {i} удалим его ')
                    os.chdir(
                        current_folder
                    )  # test print('переходим обратно') print('Теперь мы в', os.getcwd())

                    shutil.move(i, self.arhiv_order_path)
                    os.chdir(settings.MEDIA_ROOT)
                else:
                    os.chdir(current_folder)
                    shutil.move(i, self.arhiv_order_path)
                    os.chdir(settings.MEDIA_ROOT)  # Возвращаемся в корень

    def add_archive_in_order(self):
        """Записываем в таблицу ссылку на архив с файлами"""
        order = Order.objects.get(id=self.order_id)
        logger.info(
            f"Записываю в заказ ссылку на архив: archive/{self.order_id}/{self.arh_name}"
        )
        order.order_arhive = f"arhive/{self.order_id}/{self.arh_name}"
        order.save()

    def download_link(self):
        order = Order.objects.get(id=self.order_id)
        logger.info(f" LINK {order.order_arhive}")
        return order.order_arhive

    def set_status_order(self, id_status: int):
        """Меняем статус заказа"""
        order = Order.objects.get(id=self.order_id)
        status = StatusOrder.objects.get(id=id_status)  # меняю стаус
        logger.info(f"МЕНЯЮ СТАТУС ЗАКАЗА НА ОФОРМЛЕН ")
        order.status = status
        order.save()

    @staticmethod
    def calculate_signature(*args) -> str:
        """Create signature MD5.
        """
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    def __generate_link_to_work(self):
        '''Генерирую ссылку с уникальным ключом для перевода заказа в состояние в работе'''
        self.confirm_link_to_work = (f'http://{self.domain}/files/confirm_order_to_work/{self.order_id}/'
                                     f'{self.calculate_signature(self.order_id)}')
        logger.info(f'[Генерирую ссылку подтверждения принятия заказа] CONFIRM LINK: {self.confirm_link_to_work}')

    @classmethod
    def _add_white_border(cls, file_name, resolution):
        logger.info(f'[info] Увеличиваем поля на 5 см resolution {resolution} RESP {5 * resolution / 2.54}')
        img = Image.open(file_name)
        print('RES', resolution)
        border = int(5 * resolution / 2.54)  # на 5 см с каждой стороны увеличим картинку
        img_border = ImageOps.expand(img, border=border, fill='#ffffff')
        img_border.save(file_name)

    def send_msg_send_message(self):
        # ----------''' Сообщение дминистратору'''--------------
        ''' В будущем - -Сообщение менеджеру типографии'''
        admin_phone = os.getenv('PHONE_NUMBER')
        send_message_whatsapp.delay(f'{admin_phone}', f'Письмо отправлено в типографию. '
                                                      f'Заказ № {self.order_id} оформлен')

    def run(self):
        self.create_list()
        self.archive()  # архивация заказа
        self.create_folder_server()  # Создаем папку на сервере
        self.copy_files_in_server()
        self.add_archive_in_order()
        self.set_status_order(2)  # меняю статус заказа на Оформлен (статус: 2)
        self.__generate_link_to_work()  # генерирую ссылку о подтверждении принятия в работу
        self.send_mail_order()  # отправил письмо
        self.send_msg_send_message()
