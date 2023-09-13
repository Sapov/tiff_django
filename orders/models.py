import os
import shutil
import zipfile
from datetime import date

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from account.models import Organisation
from files.models import Product, StatusProduct
from django.db.models.signals import post_save
from django.urls import reverse
import subprocess
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

LOCAL_PATH_YADISK = os.getenv('LOCAL_PATH_YADISK')


class StatusOrder(models.Model):
    name = models.CharField(max_length=48, verbose_name='Status')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class Order(models.Model):
    total_price = models.FloatField(max_length=10, null=True, help_text='Стоимость заказа',
                                    verbose_name='Общая Стоимость ',
                                    blank=True)
    cost_total_price = models.FloatField(max_length=10, null=True, help_text='Себестоимость заказа',
                                         verbose_name='Общая Себестоимость ',
                                         blank=True)
    organisation_payer = models.ForeignKey(Organisation, on_delete=models.CASCADE,
                                           verbose_name='организация платильщик', help_text='Выберите организацию платильщик')
    paid = models.BooleanField(verbose_name='заказ оплачен', default=False)
    date_complete = models.DateTimeField(verbose_name='Дата готовности заказа',
                                         help_text='Введите дату к которой нужен заказ', null=True, blank=True)
    comments = models.TextField(verbose_name='Comments', blank=True)
    status = models.ForeignKey(StatusOrder, on_delete=models.CASCADE, verbose_name="Статус заказа", default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    Contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ЗАКАЗЧИК!!',
                                   default=1)

    def __str__(self):
        return f'Заказ № {self.id}  {self.organisation_payer}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'

    def get_absolute_url(self):
        return reverse('orders:add_file_in_order', args=[self.id])


def order_post_save(sender, instance, created, **kwargs):
    '''Если статус заказа  (В работе) - меняем все файлы в заказе на статус в работе '''
    status = instance.status
    id_order = instance.id
    if status.id == 2:  # Если статус "В работе"
        logger.info('in Work')
        # меняем все файлы в заказе на статус в работе
        all_products_in_order = OrderItem.objects.filter(order=id_order, is_active=True)
        for item in all_products_in_order:
            file = Product.objects.get(id=item.product.id)
            status = StatusProduct.objects.get(id=2)
            file.status_product = status
            file.save()
        # ______________ SEND FILES__________________
        order_item = UtilsModel(id_order)
        order_item.run()


post_save.connect(order_post_save, sender=Order)
# Hard

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Ордер')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    price_per_item = models.FloatField(max_length=100, help_text='За 1 шт.', verbose_name='Стоимость шт.', blank=True)
    cost_price_per_item = models.FloatField(max_length=100, help_text='За 1 шт.', verbose_name='Себестоимость шт.',
                                            blank=True, null=True)
    quantity = models.IntegerField(default=1, help_text='Введите количество', verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Себестоимость шт.',
                                           blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update

    class Meta:
        verbose_name_plural = 'Товары в заказе'
        verbose_name = 'Товар в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        logging.info('tetst', price_per_item)
        logger.info(price_per_item)
        self.price_per_item = price_per_item
        self.total_price = self.price_per_item * self.quantity
        # Cost
        cost_price_per_item = self.product.cost_price
        logger.info(f'cost_price_per_item {cost_price_per_item}')
        self.cost_price_per_item = cost_price_per_item
        self.cost_total_price = self.cost_price_per_item * self.quantity

        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order}-{self.product}'


def product_in_order_post_save(instance, **kwargs):
    order = instance.order
    all_products_in_order = OrderItem.objects.filter(order=order, is_active=True)
    order_total_price = 0
    cost_order_total_price = 0

    for item in all_products_in_order:
        order_total_price += item.total_price
        cost_order_total_price += item.cost_total_price

    instance.order.total_price = order_total_price
    instance.order.cost_total_price = cost_order_total_price
    logger.info(instance.order.total_price)
    logger.info(f'Себестоимость, {cost_order_total_price}')
    instance.order.save(force_update=True)

    # -----------
    '''Меняем состояние файла (в заказе)'''
    instance.product.in_order = True
    instance.product.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=OrderItem)


def goto_media(foo):
    ''' переходим в папку media/image{data}  и обратно'''

    def wrapper(*args, **kwargs):
        logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
        curent_path = os.getcwd()
        # logger.info(f'[INFO DECORATOR] OBJECT: {order_id}')
        # data_file = Product.objects.get(id=self.order_id)
        # logger.info(f'[INFO DECORATOR] OBJECT: {data_file}')
        # logger.info(f'[INFO DECORATOR] CREATED: {data_file.created}')

        os.chdir(
            f'{settings.MEDIA_ROOT}/image/{str(date.today())}')  # перейти в директорию дата должна браться из параметра Order.created
        logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
        res = foo(*args, **kwargs)
        os.chdir(curent_path)  # перейти обратно
        logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
        return res

    return wrapper


class UtilsModel:
    organizations = 'Style_N'
    path_save = f'{organizations}/{date.today()}'

    def __init__(self, order_id):
        self.new_str = None
        self.ya_link = None
        self.arh_name = None
        self.text_file_name = None
        self.order_id = order_id
        self.path_yandex_disk = f'{LOCAL_PATH_YADISK}{UtilsModel.path_save}/{self.order_id}'

    @staticmethod
    def arhvive(list_files: list, id_order: str) -> str:  # add tif to ZIP file
        '''Архивируем заказ'''
        if os.path.isfile(f'Order_№_{id_order}_{date.today()}.zip'):
            logger.info('Файл уже существует, архивация пропущена')
        else:
            logger.info('Архивируем файлы:')
            logger.info(f"Архивируем файлы: {list_files}")
            for name in list_files:
                arh_name = f'Order_№_{id_order}_{date.today()}.zip'
                new_arh = zipfile.ZipFile(arh_name, "a")
                new_arh.write(name, compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()
        return f'Order_№_{id_order}_{date.today()}.zip'

    def send_mail_order(self):
        ''' принимаем ссылку на яд и текст шаблон письма'''
        send_mail('Новый заказ от REDS',
                  'заказ',
                  'django.rpk@mail.ru',
                  ['rpk.reds@ya.ru'],
                  fail_silently=False,
                  html_message=f'{self.new_str}\nCсылка на архив: {self.ya_link}')

    @goto_media
    def create_text_file(self):
        ''' Создаем файл с харaктерисиками файла для печати '''

        all_products_in_order = OrderItem.objects.filter(order=self.order_id, is_active=True)
        self.text_file_name = f'Order_№{self.order_id}_for_print_{date.today()}.txt'
        with open(self.text_file_name, "w") as text_file:
            text_file.write(f'{"*" * 5}   Заказ № {self.order_id}   {"*" * 5}\n\n')
            for item in all_products_in_order:
                file = Product.objects.get(id=item.product.id)
                file_name = f'Имя файла: {str(file.images)[str(file.images).rindex("/") + 1:]}'  # обрезаем пути оставляем только имя файла
                material_txt = f'Материал для печати: {file.material}'
                quantity_print = f'Количество: {file.quantity} шт.'
                length_width = f'Ширина: {file.width} см\nДлина: {file.length} см\nРазрешение: {file.resolution} dpi'
                color_model = f'Цветовая модель: {file.color_model}'
                size = f'Размер: {file.size} Мб'
                square = f'Площадь: {(file.length * file.width) / 10000} м2'
                finish_work_rec_file = f'Финишная обработка: {file.FinishWork}'
                fields = f'Поля: {file.Fields}'

                text_file.write(
                    f'{file_name}\n{material_txt}\n{quantity_print}\n{length_width}\n{square}\n{color_model}\n{size}\n{fields}\n{finish_work_rec_file}\n'
                )
                text_file.write("-" * 40 + "\n")
        logger.info(f'CREATE File, {self.text_file_name}')

        return self.text_file_name

    def create_folder(self):
        '''Добавляем фолдер
        Директория должна быть всегда уникальной к примеру точная дата
        и номер заказа
        '''
        if os.path.exists(self.path_yandex_disk):
            logger.info(f'Директория {self.path_yandex_disk} уже создана')

        else:
            logger.info(f'Создаем Директорию {self.path_yandex_disk}')
            os.makedirs(self.path_yandex_disk)

    def add_yadisk_locate(self):
        """закидываем файлы на yadisk локально на ubuntu
        Если состояние заказа ставим обратно в ОФОРМЛЕН, а потом ставим в РАБОТЕ, то файл(архив) на
        Я-ДИСКЕ затирается новым"""
        # Path.cwd()  # Идем в текущий каталог
        os.chdir(
            f'{settings.MEDIA_ROOT}/image/{str(date.today())}')
        curent_folder = os.getcwd()
        logger.info(f'Из яндекс функции видим каталог - {curent_folder}')
        lst_files = os.listdir()  # read name files from folder
        for i in lst_files:
            if i.endswith("txt") or i.endswith("zip"):
                logger.info(f'Копирую {i} в {self.path_yandex_disk}')
                os.chdir(self.path_yandex_disk)  # перехожу в я-диск # test print('Теперь мы в', os.getcwd())
                if os.path.exists(i):
                    os.remove(i)  # test print(f'На ya Диске есть такой файл {i} удалим его ')
                    os.chdir(curent_folder)  # test print('переходим обратно') print('Теперь мы в', os.getcwd())

                    shutil.move(i, self.path_yandex_disk)
                    os.chdir(settings.MEDIA_ROOT)
                else:
                    os.chdir(curent_folder)
                    shutil.move(i, self.path_yandex_disk)
                    # Возвращаемся в корень
                    os.chdir(settings.MEDIA_ROOT)

    def add_link_from_folder_yadisk(self, path=path_save):
        logger.info(f'Публикую папку: {self.path_yandex_disk}')
        ya_link = subprocess.check_output(["yandex-disk", "publish", self.path_yandex_disk])
        ya_link = str(ya_link)
        ya_link = ya_link.lstrip("b'")
        self.ya_link = ya_link.rstrip(r"\n'")
        logger.info(f'Ссылка на яндекс диск: {self.ya_link}')
        return self.ya_link

    @goto_media
    def read_file(self):
        with open(self.text_file_name) as file:  # читаю файл txt
            self.new_str = file.read()
            return self.new_str

    @goto_media
    def arhive(self):
        """Архивируем заказ"""

        if os.path.isfile(f'Order_№_{self.order_id}_{date.today()}.zip'):
            logger.info('Файл уже существует, архивация пропущена')
        else:
            all_products_in_order = OrderItem.objects.filter(order=self.order_id, is_active=True)
            logger.info(f'Архивируем файлы:", {all_products_in_order}')
            for item in all_products_in_order:
                file = Product.objects.get(id=item.product.id)
                self.arh_name = f'Order_№_{self.order_id}_{date.today()}.zip'
                new_arh = zipfile.ZipFile(self.arh_name, "a")
                logger.info(str(file.images)[str(file.images).rindex("/") + 1:])
                new_arh.write(str(file.images)[str(file.images).rindex("/") + 1:], compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()
        return self.arh_name

    def run(self):
        self.create_text_file()
        self.read_file()
        self.arhive()  # архивация заказа
        # # --------------------------Work in Yandex Disk--------------------------------#
        self.create_folder()  # Создаем папку на yadisk с датой
        self.add_yadisk_locate()  # copy files in yadisk
        self.add_link_from_folder_yadisk()  # Опубликовал папку получил линк
        self.send_mail_order()  # отправил письмо
