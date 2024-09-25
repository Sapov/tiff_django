import hashlib
import logging
import os
import shutil
import zipfile
from datetime import date, datetime
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.urls import reverse

from account.models import Organisation, Delivery
from files.models import Product

logger = logging.getLogger(__name__)


class StatusOrder(models.Model):
    name = models.CharField(max_length=48, verbose_name="Status")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Статусы"
        verbose_name = "Статус"


class Order(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, verbose_name='Доставка', null=True, default=3)
    total_price = models.FloatField(max_length=10, null=True, help_text="Стоимость заказа",
                                    verbose_name="Общая Стоимость", blank=True, )
    cost_total_price = models.FloatField(
        max_length=10,
        null=True,
        help_text="Себестоимость заказа",
        verbose_name="Общая Себестоимость",
        blank=True,
    )
    organisation_payer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name="Организация плательщик",
        help_text="Выберите организацию плательщик",
        null=True,
        blank=True,
        default=1
    )
    paid = models.BooleanField(verbose_name="Заказ оплачен", default=False)
    date_complete = models.DateTimeField(
        verbose_name="Дата готовности заказа",
        help_text="Введите дату к которой нужен заказ",
        null=True,
        blank=True,
    )
    comments = models.TextField(verbose_name="Комментарии к заказу", blank=True)
    status = models.ForeignKey(
        StatusOrder, on_delete=models.CASCADE, verbose_name="Статус заказа", default=1
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    Contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ЗАКАЗЧИК!!",
        default=1,
    )
    order_arhive = models.FileField(upload_to=f"arhive/{id}", null=True, blank=True)
    order_pdf_file = models.FileField(upload_to=f"orders/", null=True, blank=True)
    pay_link = models.TextField(verbose_name='ссылка для оплаты', null=True, blank=True)

    def __str__(self):
        return f"Заказ № {self.id}"

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

    def get_absolute_url(self):
        return reverse("orders:add_file_in_order", args=[self.id])


# def order_post_save(sender, instance, created, **kwargs):
#     """Если статус заказа (В работе) - меняем все файлы в заказе на статус в работе"""
#     status = instance.status
#     id_order = instance.id
#     if status.id == 2:  # Если статус "В работе"
#         logger.info("in Work")
#         # меняем все файлы в заказе на статус в работе
#         all_products_in_order = OrderItem.objects.filter(order=id_order, is_active=True)
#         for item in all_products_in_order:
#             file = Product.objects.get(id=item.product.id)
#             status = StatusProduct.objects.get(id=2)
#             file.status_product = status
#             file.save()
#         # ______________ SEND FILES__________________
#         # order_item = UtilsModel(id_order)
#         # order_item.run()
#
#
# post_save.connect(order_post_save, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Ордер")
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    price_per_item = models.FloatField(
        max_length=100, help_text="За 1 шт.", verbose_name="Стоимость шт.", blank=True
    )
    cost_price_per_item = models.FloatField(
        max_length=100,
        help_text="За 1 шт.",
        verbose_name="Себестоимость шт.",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(
        default=1, help_text="Введите количество", verbose_name="Количество"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Себестоимость шт.",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )  # date created
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Изменено"
    )  # date update

    class Meta:
        verbose_name_plural = "Товары в заказе"
        verbose_name = "Товар в заказе"

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        logger.info(price_per_item)
        self.price_per_item = price_per_item
        self.total_price = self.price_per_item * self.quantity
        # Cost
        cost_price_per_item = self.product.cost_price
        logger.info(f"cost_price_per_item {cost_price_per_item}")
        self.cost_price_per_item = cost_price_per_item
        self.cost_total_price = self.cost_price_per_item * self.quantity

        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}-{self.product}"


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
    logger.info(f"Себестоимость, {cost_order_total_price}")
    instance.order.save(force_update=True)

    # -----------
    """Меняем состояние файла (в заказе)"""
    instance.product.in_order = True
    instance.product.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=OrderItem)


# def goto_media(foo):
#     ''' переходим в папку media/image{data}  и обратно'''
#
#     def wrapper(*args, **kwargs):
#         logger.info(f'[INFO DECORATOR] перед работой мы тут: {os.getcwd()}')
#         current_path = os.getcwd()
#         os.chdir(f'{settings.MEDIA_ROOT}/image/{str(date.today())}')
#         # перейти в директорию дата должна браться из параметра Order.created
#         logger.info(f'[INFO DECORATOR] Мы Выбрали: {os.getcwd()}')
#         res = foo(*args, **kwargs)
#         os.chdir(current_path)  # перейти обратно
#         logger.info(f'[INFO DECORATOR] Возвращаемся обратно: {os.getcwd()}')
#         return res
#
#     return wrapper


class UtilsModel:
    def __init__(self, order_id, domain):
        self.order_complete = None
        self.order_list = None
        self.hash_num = None
        self.arhiv_order_path = None
        self.new_str = None
        self.arh_name = None
        self.text_file_name = None
        self.order_id = order_id
        self.path_arhive = f"{settings.MEDIA_ROOT}/arhive"
        self.domain = domain
        self.confirm_link_to_work = None
        self.confirm_link_to_complited = None

    def send_mail_order(self):
        """отправляем письмо с архивом подрядчику"""
        order = Order.objects.get(id=self.order_id)
        data = {
            "data_order_complete": self.order_complete,
            "order_item": self.order_list,
            "order_archive_link": f"http://{self.domain}/media/{str(order.order_arhive)}",
            "confirm_link": self.confirm_link_to_work,
            "confirm_status_complete": self.confirm_link_to_complited,
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

    def create_text_file(self):
        """Создаем файл с харaктеристеками файла для печати"""
        current_path = os.getcwd()
        os.chdir(f"{settings.MEDIA_ROOT}/image/")

        all_products_in_order = OrderItem.objects.filter(order=self.order_id, is_active=True)
        order = Order.objects.get(id=self.order_id)
        self.order_complete = order.date_complete - datetime.timedelta(hours=24)  # Типография от дает на сутки раньше

        self.text_file_name = f"Order_№{self.order_id}_for_print_{date.today()}.txt"
        with open(self.text_file_name, "w") as text_file:
            text_file.write(f'{"*" * 5}   Заказ № {self.order_id}   {"*" * 5}\n\n')
            self.order_list = []
            items_file = {}
            for item in all_products_in_order:
                file = Product.objects.get(id=item.product.id)
                file_name = f'Имя файла: {str(file.images)[str(file.images).rindex("/") + 1:]}'  # обрезаем пути оставляем только имя файла
                material_txt = f"Материал для печати: {file.material}"
                quantity_print = f"Количество: {file.quantity} шт."
                length_width = f"Ширина: {file.width} м\nДлина: {file.length} м\nРазрешение: {file.resolution} dpi"
                color_model = f"Цветовая модель: {file.color_model}"
                size = f"Размер: {file.size} Мб"
                square = f"Площадь: {(file.length * file.width)} м2"
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

                text_file.write(
                    f"{file_name}\n{material_txt}\n{quantity_print}\n{length_width}\n{square}\n{color_model}\n{size}\n{finish_work_rec_file}\n{comments}\n"
                )
                text_file.write("-" * 40 + "\n")
        logger.info(f"CREATE File, {self.text_file_name}")
        logger.info(f"CREATE LIST, {self.order_list}")

        os.chdir(current_path)
        return self.text_file_name

    def read_file(self):
        current_path = os.getcwd()  # запоминаем где мы
        os.chdir(f"{settings.MEDIA_ROOT}/image/")  # перейти в директорию image
        with open(self.text_file_name) as file:  # читаю файл txt
            self.new_str = file.read()
            os.chdir(current_path)  # перейти обратно

            return self.new_str

    def arhive(self):
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
                file = Product.objects.get(id=item.product.id)
                logger.info(f"FILE: {file}")
                self.arh_name = f"Order_№_{self.order_id}_{date.today()}.zip"
                new_arh = zipfile.ZipFile(self.arh_name, "a")

                logger.info(f'----------------Формируем имя файла типа | 5_шт_100х200_Баннер_510_грамм_|------------')
                new_name_file = (f"{file.quantity}_шт_{float(file.width)}x{float(file.length)}_"
                                 f"{'_'.join(str(file.material).split())}_"
                                 f"{'_'.join(str(file.FinishWork).split())}_{file.id}{str(file.images)[-4:]}")
                logger.info(f'[new Name] {new_name_file}')
                logger.info(f'file.images: {file.images}')

                logger.info(f'[OLD name] {str(file.images)[str(file.images).rindex("/") + 1:]}')
                old_name = str(file.images)[str(file.images).rindex("/") + 1:]

                # os.rename(old_name, new_name_file)
                shutil.copy(old_name, new_name_file)
                new_arh.write(new_name_file, compress_type=zipfile.ZIP_DEFLATED)
                new_arh.close()
        os.chdir(current_path)  # перейти обратно
        return self.arh_name

    def create_folder_server(self):
        """Добавляем фолдер  Директория номер заказа"""
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

    def add_arhive_in_order(self):
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

    def set_status_file(self):
        '''Меняем стаус файла на "в работе"'''
        pass

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

    def run(self):
        self.create_text_file()
        self.read_file()
        self.arhive()  # архивация заказа
        self.create_folder_server()  # Создаем папку на сервере
        self.copy_files_in_server()
        self.add_arhive_in_order()
        self.set_status_order(2)  # меняю статус заказа на Оформлен (статус: 2)
        self.__generate_link_to_work()  # генерирую ссылку о подтверждении принятия в работу
        self.send_mail_order()  # отправил письмо


class BankInvoices(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    document_id = models.CharField(max_length=40, verbose_name='Номер выставленного документа в банке')
    payment_Status = models.CharField(max_length=40, verbose_name='Статус оплаты', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
