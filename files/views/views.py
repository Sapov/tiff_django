import os
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseNotFound, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from orders.alerts import Alerts
from orders.models import Order, StatusOrder, OrderItem
from files.works_with_files.atchives_files import UtilsModel
from orders.views import change_status_order, get_domain, set_status_file
from files.models import Product, Material, FinishWork, UseCalculator, Contractor, StatusProduct, FileUpload
from files.forms import (
    CalculatorForm,
    UploadFilesInter,
    UploadFilesLarge,
    UploadFilesUV,
    UploadFilesRollUp, CalculatorLargePrint, CalculatorInterierPrint, CalculatorUVPrint, CalculatorBlankMaterial,
    UploadFilesPictures, UploadFileForm,
)
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin  # new

from files.tiff_file import Calculator
from rest_framework import viewsets
from files.serializers import MaterlailSerializer

from users.tasks import send_message_whatsapp
from files.tasks import resize_image, process_large_file
from django.http import JsonResponse
from files.tasks import process_uploaded_file

import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Вывод файлов только авторизованного пользователя"""
    # вывод в обратном порядке -id
    object_list = Product.objects.filter(user=request.user).order_by("-id")
    """paginator"""
    paginator = Paginator(object_list, 5)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {"object_list": object_list, "title": "Ваши файлы", "page_obj": page_obj},
    )


class ViewFilesUserListView(LoginRequiredMixin, ListView):
    """Посмотреть все файлы пользователя"""

    model = Product
    paginate_by = 5
    template_name = "index.html"
    login_url = "login"

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user).order_by("-id")
        return queryset


def delete(request, id):
    try:
        product = Product.objects.get(id=id)  # выбрали запись
        # Deleting files

        os.remove(f"media/{str(product.images)}")  # Удаление файла
        product.delete()
        # удалили запись
        return HttpResponseRedirect("/files/")
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Удаление</h2>")


class FilesUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["quantity", "material", "FinishWork"]
    template_name = "product_update_form.html"
    login_url = "login"


def handle_uploaded_file(f):
    with open(f"media/uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class FilesCreateView(LoginRequiredMixin, FormView):
    model = Product
    fields = ["quantity", "material", "FinishWork", "images", "comments"]
    template_name = 'files/upload_files.html'
    success_url = 'files:myfiles'

    def form_valid(self, form):
        file = form.cleaned_data['files']
        handle_uploaded_file(file)
        print(file)
        return super().form_valid(form)




@login_required
def price(request):
    """Вывод прайс-листа"""
    price_shirka = Material.objects.filter(type_print=1)  # Только широкоформатная печать!!!
    price_interierka = Material.objects.filter(type_print=2)  # Только Интерьерная печать!!!
    price_UV = Material.objects.filter(type_print=3)  # Только UV печать!!!
    blank_material = Material.objects.filter(type_print=4)  # Только Чистый материал!!!
    pictures = Material.objects.filter(type_print=5)  # Это картины на подрамнике!!!
    finishka = FinishWork.objects.all()  # Только финишка печать!!!
    return render(
        request,
        "price.html",
        {
            "price_shirka": price_shirka,
            "price_interierka": price_interierka,
            "price_UV": price_UV,
            "finishka": finishka,
            "pictures": pictures,
            'blank_material': blank_material,
            "title": "Прайс-лист",
        },
    )


def calculator(request):
    last_five_string = last_ten_string()
    title = "Калькулятор широкоформатной печати"
    template_name = "files/calculator.html"

    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user  # Хочу передавать словарем
            cd['role'] = request.user.role
            logger.info(f'[INFO CLEAN DATA] {cd}')
            image_price = Calculator(cd)
            results = image_price.calculate_price()
            cd['results'] = results
            try:
                add_item_calculator(cd)
                return render(request, template_name, {"form": form,
                                                       "title": title,
                                                       "results": results,
                                                       'last_five_string': last_five_string,
                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorForm()
        return render(request, template_name,
                      {"form": form, "title": title,
                       'last_five_string': last_five_string})


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<H1>Страница не найдена</H1")


class BaseFilesCreateView(LoginRequiredMixin, CreateView):
    """Базовый класс для загрузки файлов"""
    model = Product
    template_name = "files/large_print.html"
    success_url = "files:about_file"

    def form_valid(self, form):
        form.instance.user = self.request.user
        instance = form.save()

        task = process_uploaded_file.delay(
            file_path=instance.images.path,
            user_id=self.request.user.id
        )

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'task_id': task.id})

        return super().form_valid(form)


class FilesCreateViewInter(BaseFilesCreateView):
    """Загрузка файлов только для интерьерной печати"""
    form_class = UploadFilesInter

class FilesCreateViewUV(BaseFilesCreateView):
    """Загрузка файлов только для UV печати"""
    form_class = UploadFilesUV


class FilesCreateViewLarge(BaseFilesCreateView):
    """Загрузка файлов для широкоформатной печати"""
    form_class = UploadFilesLarge


class FilesCreateViewRollUp(BaseFilesCreateView):
    """Загрузка файлов только для Rollup"""
    form_class = UploadFilesRollUp
    template_name = "files/rollup_print.html"


class PicturesCreateViewInter(BaseFilesCreateView):
    """Загрузка файлов  для Картин на холсте печати"""
    form_class = UploadFilesPictures
    template_name = "files/pictures_print.html"


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterlailSerializer


def calculator_large_print_out(request):
    last_five_string = last_ten_string()
    title = "Калькулятор широкоформатной печати"
    template_name = "files/calculator_large.html"

    if request.method == 'POST':
        form = CalculatorLargePrint(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user  # Хочу передавать словарем
            cd['role'] = request.user

            logger.info(f'[--INFO CLEAN DATA--] {cd}')
            image_price = Calculator(cd)
            results, st_discount = image_price.discount()
            cd['results'] = results
            try:
                add_item_calculator(cd)
            except:
                print(ValueError)
            try:
                return render(request, template_name, {"form": form,
                                                       "title": title,
                                                       "results": results,
                                                       'st_discount': st_discount,
                                                       'last_five_string': last_five_string,
                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorLargePrint()
        return render(request, template_name,
                      {"form": form, "title": title,
                       'last_five_string': last_five_string})


def add_item_calculator(cd):
    if str(cd['user']) == "AnonymousUser":
        UseCalculator.objects.create(material=cd['material'], quantity=int(cd['quantity']),
                                     width=cd['width'], length=cd['length'],
                                     results=cd['results'], FinishWork=cd['finishing'],
                                     )
    else:
        UseCalculator.objects.create(material=cd['material'], quantity=int(cd['quantity']),
                                     width=cd['width'], length=cd['length'],
                                     results=cd['results'], FinishWork=cd['finishing'],
                                     user=cd['user'])


def calculator_interior_print(request):
    last_five_string = last_ten_string()
    title = "Калькулятор Интерьерной печати"
    template_name = "files/calculator_large.html"

    if request.method == 'POST':
        form = CalculatorInterierPrint(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user  # Хочу передавать словарем
            cd['role'] = request.user
            logger.info(f'[INFO CLEAN DATA] {cd}')
            image_price = Calculator(cd)
            results = image_price.calculate_price()
            cd['results'] = results
            try:
                add_item_calculator(cd)
                return render(request, template_name, {"form": form,
                                                       "title": title,
                                                       "results": results,
                                                       'last_five_string': last_five_string,
                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorInterierPrint()
        return render(request, template_name,
                      {"form": form, "title": title,
                       'last_five_string': last_five_string})


def calculator_uv_print_out(request):
    """ Калькулятор для УФ печати"""
    last_five_string = last_ten_string()
    title = 'Калькулятор UV печати'
    template_name = "files/calculator_large.html"

    if request.method == 'POST':
        form = CalculatorUVPrint(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user  # Хочу передавать словарем
            cd['role'] = request.user
            logger.info(f'[INFO CLEAN DATA] {cd}')
            image_price = Calculator(cd)
            results = image_price.calculate_price()
            cd['results'] = results
            try:
                add_item_calculator(cd)
                return render(request, template_name, {"form": form,
                                                       "title": title,
                                                       "results": results,
                                                       'last_five_string': last_five_string,
                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorUVPrint()
        return render(request, template_name,
                      {"form": form, "title": title,
                       'last_five_string': last_five_string})


def calculator_blank_out(request):
    """ Калькулятор чистого материала"""
    last_five_string = last_ten_string()
    title = 'Калькулятор Чистый материал'
    template_name = "files/calculator_large.html"

    if request.method == 'POST':
        form = CalculatorBlankMaterial(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user  # Хочу передавать словарем
            cd['role'] = request.user
            logger.info(f'[INFO CLEAN DATA] {cd}')
            image_price = Calculator(cd)
            results = image_price.calculate_price()
            cd['results'] = results
            try:
                add_item_calculator(cd)
                return render(request, template_name, {"form": form,
                                                       "title": title,
                                                       "results": results,
                                                       'last_five_string': last_five_string,
                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorBlankMaterial()
        return render(request, template_name,
                      {"form": form, "title": title,
                       'last_five_string': last_five_string})


def last_ten_string():
    last_five_string = UseCalculator.objects.order_by('-id')[:10]
    return last_five_string


class ViewContractorListView(LoginRequiredMixin, ListView):
    """Посмотреть всех подрядчиков"""
    model = Contractor
    # paginate_by = 5
    template_name = "files/view_contractor.html"
    login_url = "login"


class ContractorCreateView(LoginRequiredMixin, CreateView):
    """Добавить подрядчика"""
    model = Contractor
    fields = ["name", "description", "email_contractor", "phone_contractor", "phone_contractor_2",
              'address', 'contact_contractor']

    # только для текущего юзера
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContractorUpdateView(UpdateView):
    model = Contractor
    fields = ["name", "description", "email_contractor", "phone_contractor", "phone_contractor_2",
              'address', 'contact_contractor']
    template_name_suffix = "_update_form"


class ContractorDeleteView(DeleteView):
    model = Contractor
    success_url = reverse_lazy("files:contractor_view")


def confirm_order_to_work(request, pk: int, hash_code: str):
    ''' Подтверждение приема заказа менеджером типографии'''
    if hash_code == UtilsModel.calculate_signature(pk):  # Нужно проверить что хеш равен коду от хеша номера заказа
        """Меняем статус заказа"""
        if change_status_order(3, pk):
            # оповещаем в whatsapp
            send_message_whatsapp.delay(f'{os.getenv("PHONE_NUMBER")}', f'Заказ № {pk} Принят типографией')

            context = Alerts.view_items_in_order(pk)

            return render(request, "files/confirm_order_to_work.html", context)
        else:
            return render(request, "files/order_already_recorded.html", {'message': 'Заказ уже В работе!'})

    else:
        return render(request, "files/no_confirm_order_to_work.html")


def confirm_order_to_completed(request, pk: int, hash_code):
    ''' Подтверждение готовности заказа менеджером типографии'''
    if request.method == 'GET':
        if hash_code == UtilsModel.calculate_signature(pk):  # Нужно проверить что хеш  равен коду от хеша номера заказа
            """Меняем статус заказа"""
            if change_status_order(5, pk):  # Статус Готов
                Alerts.stop_count_down(pk)
                # Отослать сообщение админу и клиенту на месенджер
                send_message_whatsapp.delay(f'{os.getenv("PHONE_NUMBER")}',
                                            f'Типография подтвердила готовность заказа № {pk}')
                files_new_status(pk)
                return render(request, "files/confirm_order_to_completed.html")
            else:
                return render(request, "files/order_already_recorded.html", {'message':'Заказ уже закрыт!'})
        else:
            return render(request, "files/no_confirm_order_to_completed.html")

def files_new_status(order_id:int):
    '''Функция меняет статус файлов на "В архиве"'''
    all_products_in_order = OrderItem.objects.filter(order=order_id)
    for i in all_products_in_order:
        set_status_file(i.product, 4)
        print('STATUS---', i.product.status_product)







def add_time_order(request, pk: int, hash_code):
    '''Добавление времени на исполнение текущего заказа'''
    if request.method == 'GET':
        if hash_code == UtilsModel.calculate_signature(pk):  # коду от хеша номера заказа
            items_in_order = OrderItem.objects.filter(order=pk)  # файлы в заказе
            order = Order.objects.get(id=pk)
            context = {
                "items_in_order": items_in_order,
                "order_id": pk,
                'old_data': order.date_complete,
                'today': datetime.today().strftime('%Y-%m-%dT%H:%M')
            }
            return render(request, 'files/add_time_order.html', context)
    elif request.method == 'POST':
        my_date = request.POST["date"]
        order = Order.objects.get(id=pk)
        old_data = order.date_complete
        set_data = datetime.strptime(my_date, '%Y-%m-%dT%H:%M')
        order.date_complete = set_data
        order.save()
        new_data = order.date_complete
        context = {
            'old_data': old_data,
            'new_data': new_data,
            "order_id": pk,
        }
        domain = str(get_domain(request))
        Alerts.set_time_count_down(pk, domain)
        return render(request, 'files/add_time_order_set.html', context)


def about_file(request, file_id):
    file = Product.objects.get(id=file_id)
    # print(f'Разрешение файла {file.resolution} VS Разрешение печати {file.material.resolution_print}') file.material
    # if file.resolution < file.material.resolution_print:
    #     message = (f"Файл не подходит для качественной печати. Разрешение файла {file.resolution} dpi меньше "
    #                f"положенного {file.material.resolution_print} dpi")
    # elif file.resolution > file.material.resolution_print:
    #
    # else:
    message = ''

    return render(request, "files/about_file.html", {"file": file, 'message': message})


class PicturesListView(LoginRequiredMixin, ListView):
    """Посмотреть стоимость печати картин на подрамнике"""

    model = Material
    # paginate_by = 5
    template_name = "files/pictures.html"
    login_url = "login"

    def get_queryset(self):
        return Material.objects.filter(type_print=5)  # Это картины на подрамнике!!!


class CalculatorLIst(LoginRequiredMixin, ListView):
    '''Вывести расчеты тольео конкретного пользователя'''
    model = UseCalculator
    paginate_by = 5
    template_name = "files/calculator_list.html"
    login_url = "login"

    def get_queryset(self):
        print(self.request.user)
        queryset = UseCalculator.objects.filter(user=self.request.user).order_by("-id")
        return queryset



def upload_file(request):
    if request.method == 'POST':
        print(request)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload = FileUpload(file=request.FILES['file'])
            upload.save()

            # Запуск асинхронной задачи
            process_large_file.delay(upload.id)

            return JsonResponse({
                'status': 'success',
                'upload_id': upload.id,
                'task_status_url': f'/upload/status/{upload.id}/'
            })
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html', {'form': form})


def upload_status(request, upload_id):
    upload = FileUpload.objects.get(id=upload_id)
    return JsonResponse({
        'status': upload.status,
        'progress': upload.progress,
        'result': upload.result
    })

import os
import zipfile
from django.shortcuts import render, redirect
from django.conf import settings
from files.forms import UploadFileForm
from files.models import UploadedFile


def upload_archive(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archive = request.FILES['file']

            # Сохраняем оригинальный архив
            archive_model = UploadedFile(
                original_archive=archive,
                file_name=archive.name,
                file_path='',  # Заполним позже
                size=archive.size
            )
            archive_model.save()

            # Путь для сохранения распакованных файлов
            extract_to = os.path.join(settings.MEDIA_ROOT, 'unpacked_files', str(archive_model.id))
            os.makedirs(extract_to, exist_ok=True)

            # Временный путь для сохранения архива
            archive_path = os.path.join(settings.MEDIA_ROOT, 'archives', archive.name)
            with open(archive_path, 'wb+') as destination:
                for chunk in archive.chunks():
                    destination.write(chunk)

            # Распаковка архива
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

            # Сохранение информации о каждом файле
            for root, dirs, files in os.walk(extract_to):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)

                    UploadedFile.objects.create(
                        file_name=file,
                        file_path=relative_path,
                        size=os.path.getsize(file_path)
                    )

            return redirect('upload_success')
    else:
        form = UploadFileForm()

    return render(request, 'files/upload.html', {'form': form})

