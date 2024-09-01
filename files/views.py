import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseNotFound, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from orders.models import UtilsModel, Order, StatusOrder
from orders.views import stop_count_down
from .models import Product, Material, FinishWork, UseCalculator, Contractor
from .forms import (
    UploadArhive,
    CalculatorForm,
    UploadFilesInter,
    UploadFilesLarge,
    UploadFilesUV,
    UploadFilesRollUp, CalculatorLargePrint, CalculatorInterierPrint, CalculatorUVPrint, CalculatorBlankMaterial,

)
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin  # new

from .tiff_file import WorkZip, Calculator
from rest_framework import viewsets
from .serializers import MaterlailSerializer

import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Вывод файлов только авторизованного пользователя"""
    # вывод в обратном порядке -id
    object_list = Product.objects.filter(Contractor=request.user).order_by("-id")
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
        queryset = Product.objects.filter(Contractor=self.request.user).order_by("-id")


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


class FilesCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["quantity", "material", "FinishWork", "images", "comments"]

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def price(request):
    """Вывод прайс-листа"""
    price_shirka = Material.objects.filter(
        type_print=1
    )  # Только широкоформатная печать!!!
    price_interierka = Material.objects.filter(type_print=2)  # Только Интерьерная печать!!!
    price_UV = Material.objects.filter(type_print=3)  # Только UV печать!!!
    blank_material = Material.objects.filter(type_print=4)  # Только Чистый материал!!!
    finishka = FinishWork.objects.all()  # Только финишка печать!!!
    return render(
        request,
        "price.html",
        {
            "price_shirka": price_shirka,
            "price_interierka": price_interierka,
            "price_UV": price_UV,
            "finishka": finishka,
            'blank_material': blank_material,
            "title": "Прайс-лист",
        },
    )


def add_files_in_base():
    print("где я", os.getcwd())
    os.path.relpath("unzip")
    list_files = os.listdir("unzip")
    print(list_files)
    print(os.path.relpath("unzip"))
    return list_files


def upload_arh(request):
    if request.POST:
        form = UploadArhive(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data['path_file'])
            file_name = form.cleaned_data["path_file"]
            form.save()
            WorkZip.print(file_name)
            WorkZip.unzip(file_name)
            WorkZip.unzip_files()

            return HttpResponseRedirect("/")
    else:
        form = UploadArhive

    return render(
        request, "files/upload_arh.html", {"form": form, "title": "Добавление файлов"}
    )  # изменение данных в БД


def calculator(request):
    if request.POST:
        form = CalculatorForm(request.POST)
        if form.is_valid():
            form = CalculatorForm(request.POST)
            length = request.POST["length"]
            width = request.POST["width"]
            quantity = request.POST["quantity"]
            material = request.POST["material"]
            finishka = request.POST["finishka"]
            logger.info(f'[USER ROLE] -> {request.user.role}')
            materials = Material.objects.get(id=material)
            finishkas = FinishWork.objects.get(id=finishka)
            perimetr = (float(width) + float(length)) * 2

            # проверка ретейл или агентство
            if request.user.role == "CUSTOMER_RETAIL":
                material_price = materials.price_customer_retail
                finishka_price = finishkas.price_customer_retail
            elif request.user.role == "CUSTOMER_AGENCY":
                material_price = materials.price
                finishka_price = finishkas.price

        finishka_price = perimetr * finishka_price
        results = (
                          float(width) * float(length) * material_price
                  ) + finishka_price  # в см
        results = round(results, -1) * int(quantity)
        if request.user.role == "CUSTOMER_RETAIL":
            if (
                    results < 1000
            ):  # если сумма получилась менее 1000 руб. округляю до 1000 руб.
                results = 1000
        return render(
            request,
            "calculator.html",
            {
                "form": form,
                "title": "Калькулятор печати",
                "results": results,
            },
        )

    else:
        form = CalculatorForm()
        return render(
            request,
            "calculator.html",
            {"form": form, "title": "Калькулятор печати"},
        )


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<H1>Страница не найдена</H1")


class FilesCreateViewInter(LoginRequiredMixin, CreateView):
    """Загрузка файлов только для интерьерной печати"""

    model = Product
    form_class = UploadFilesInter
    template_name = "files/inter_print.html"

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class FilesCreateViewLarge(LoginRequiredMixin, CreateView):
    """Загрузка файлов только для широкоформатной печати"""
    model = Product
    form_class = UploadFilesLarge
    template_name = "files/large_print.html"

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class FilesCreateViewUV(LoginRequiredMixin, CreateView):
    """Загрузка файлов только для широкоформатной печати"""

    model = Product
    form_class = UploadFilesUV
    template_name = "files/uv_print.html"

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class FilesCreateViewRollUp(LoginRequiredMixin, CreateView):
    """Загрузка файлов только для Rollup"""

    model = Product
    form_class = UploadFilesRollUp
    template_name = "files/rollup_print.html"

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterlailSerializer


def calculator_large_print_out(request):
    last_five_string = UseCalculator.objects.order_by('-id')[:5]
    if request.method == 'POST':
        form = CalculatorLargePrint(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['role'] = request.user # Хочу передавать словарем
            logger.info(f'[INFO CLEAN DATA] {cd}')
            image_price = Calculator(cd)
            results = image_price.calculate_price()
            try:
                UseCalculator.objects.create(material=cd['material'], quantity=int(cd['quantity']),
                                             width=cd['width'], length=cd['length'],
                                             results=results, FinishWork=cd['finishing'])
                return render(request, "files/calculator_large.html", {"form": form,
                                                                       "title": "Калькулятор широкоформатной печати",
                                                                       "results": results,
                                                                       'last_five_string': last_five_string,
                                                                       }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorLargePrint()
        return render(request, "files/calculator_large.html",
                      {"form": form, "title": "Калькулятор широкоформатной печати",
                       'last_five_string': last_five_string})


def calculator_interior_print(request):
    if request.method == 'POST':
        form = CalculatorInterierPrint(request.POST)
        if form.is_valid():
            length = request.POST["length"]
            width = request.POST["width"]
            quantity = request.POST["quantity"]
            material = request.POST["material"]
            finishka = request.POST["finishka"]
            materials = Material.objects.get(id=material)
            finishkas = FinishWork.objects.get(id=finishka)
            perimetr = (float(width) + float(length)) * 2
            logger.info(f'[request]:{request.POST}')
            print(form.cleaned_data)
            material_price = materials.price_customer_retail
            finishka_price = finishkas.price_customer_retail
            finishka_price = perimetr * finishka_price
            results = (float(width) * float(length) * material_price) + finishka_price  # в см
            results = round(results, -1) * int(quantity)
            if results < 1000:  # если сумма получилась менее 1000 руб. округляю до 1000 руб.
                results = 1000

            try:
                UseCalculator.objects.create(material=materials, quantity=quantity, width=width, length=length,
                                             results=results, FinishWork=finishkas)
                last_five_string = UseCalculator.objects.order_by('-id')[:5]
                return render(request, "files/calculator_interior_print.html", {"form": form,
                                                                                "title": "Калькулятор широкоформатной печати",
                                                                                "results": results,
                                                                                'last_five_string': last_five_string,
                                                                                }, )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorInterierPrint()
        last_five_string = UseCalculator.objects.order_by('-id')[:5]
        return render(request, "files/calculator_interior_print.html",
                      {"form": form, "title": "Калькулятор интерьерной печати", 'last_five_string': last_five_string})


def calculator_uv_print_out(request):
    """ Калькулятор для УФ печати"""
    if request.method == 'POST':
        form = CalculatorUVPrint(request.POST)
        if form.is_valid():
            length = request.POST["length"]
            width = request.POST["width"]
            quantity = request.POST["quantity"]
            material = request.POST["material"]
            finishka = request.POST["finishka"]
            materials = Material.objects.get(id=material)
            finishkas = FinishWork.objects.get(id=finishka)
            perimetr = (float(width) + float(length)) * 2
            logger.info(f'[request]:{request.POST}')
            print(form.cleaned_data)
            material_price = materials.price_customer_retail
            finishka_price = finishkas.price_customer_retail
            finishka_price = perimetr * finishka_price
            results = (float(width) * float(length) * material_price) + finishka_price  # в см
            results = round(results, -1) * int(quantity)
            if (results < 1000):  # если сумма получилась менее 1000 руб. округляю до 1000 руб.
                results = 1000

            try:
                UseCalculator.objects.create(material=materials, quantity=quantity, width=width, length=length,
                                             results=results, FinishWork=finishkas)
                last_five_string = UseCalculator.objects.order_by('-id')[:5]

                return render(request, "files/calculator_large.html", {"form": form,
                                                                       "title": "Калькулятор UV печати",
                                                                       "results": results,
                                                                       'last_five_string': last_five_string
                                                                       },
                              )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorUVPrint()
        last_five_string = UseCalculator.objects.order_by('-id')[:5]

        return render(
            request,
            "files/calculator_large.html",
            {"form": form, "title": "Калькулятор UV печати", 'last_five_string': last_five_string},
        )


def calculator_blank_out(request):
    """ Калькулятор чистого материала"""
    if request.method == 'POST':
        form = CalculatorBlankMaterial(request.POST)
        if form.is_valid():
            length = request.POST["length"]
            width = request.POST["width"]
            quantity = request.POST["quantity"]
            material = request.POST["material"]
            finishka = request.POST["finishka"]
            materials = Material.objects.get(id=material)
            finishkas = FinishWork.objects.get(id=finishka)
            perimetr = (float(width) + float(length)) * 2
            logger.info(f'[request]:{request.POST}')
            print(form.cleaned_data)
            material_price = materials.price_customer_retail
            finishka_price = finishkas.price_customer_retail
            finishka_price = perimetr * finishka_price
            results = (float(width) * float(length) * material_price) + finishka_price  # в см
            results = round(results, -1) * int(quantity)
            if (results < 1000):  # если сумма получилась менее 1000 руб. округляю до 1000 руб.
                results = 1000

            try:
                UseCalculator.objects.create(material=materials, quantity=quantity, width=width, length=length,
                                             results=results, FinishWork=finishkas)
                last_five_string = UseCalculator.objects.order_by('-id')[:5]

                return render(request, "files/calculator_large.html", {"form": form,
                                                                       "title": "Калькулятор пустого материала",
                                                                       "results": results,
                                                                       'last_five_string': last_five_string
                                                                       },
                              )

            except:
                form.add_error(None, 'Ошибка расчета')

    else:
        form = CalculatorBlankMaterial()
        last_five_string = UseCalculator.objects.order_by('-id')[:5]
        return render(
            request,
            "files/calculator_large.html",
            {"form": form, "title": "Калькулятор пустого материала", 'last_five_string': last_five_string},
        )


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
        form.instance.Contractor = self.request.user
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
    # print(f'id_status_order P{id_status_order} type {type(id_status_order)}')
    ''' Подтверждение приема заказа менеджером типографии'''
    if hash_code == UtilsModel.calculate_signature(pk):  # Нужно проверить что хеш равен коду от хеша номера заказа
        """Меняем статус заказа"""
        order = Order.objects.get(id=pk)  # получаем заказ по id заказаки
        status = StatusOrder.objects.get(id=3)  # меняем статус заказак)  # меняю стаус 3
        logger.info(f"МЕНЯЮ СТАТУС нА В Работе")
        order.status = status
        order.save()

        return render(request, "files/confirm_order_to_work.html")
    else:
        return render(request, "files/no_confirm_order_to_work.html")


def confirm_order_to_completed(request, pk: int, hash_code):
    ''' Подтверждение готовнасти заказа менеджером типографии'''
    if hash_code == UtilsModel.calculate_signature(pk):  # Нужно проверить что хеш  равен коду от хеша номера заказа
        """Меняем статус заказа"""
        order = Order.objects.get(id=pk)  # получаем заказ по id заказаки
        status = StatusOrder.objects.get(id=5)  # меняем статус заказак)  # меняю стаус ГОТОВ
        logger.info(f"МЕНЯЮ СТАТУС НА В ГОТОВ")
        order.status = status
        order.save()
        stop_count_down(pk)

        return render(request, "files/confirm_order_to_completed.html")
    else:
        return render(request, "files/no_confirm_order_to_completed.html")
