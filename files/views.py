import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseNotFound, request
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from orders.models import OrderItem
from .models import Product, Material, FinishWork
from .forms import AddFiles, UploadArhive, Calculator, UploadFilesInter
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin  # new
import patoolib

from .tiff_file import WorkZip


# from django.core.files.storage import FileSystemStorage
@login_required
def index(request):
    """Вывод файлов только авторизованного пользователя"""
    object_list = Product.objects.filter(Contractor=request.user).order_by(
        "-id"
    )  # вывод в обратном порядке -id
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
    paginate_by = 2
    template_name = "index.html"
    login_url = "login"

    # def get_queryset(self):
    #     queryset = Product.objects.filter(Contractor=request.h("user")).order_by(
    #         "-id"
    #     )
    #     # Product.objects.filter(Contractor=request.user).order_by('-id')  # вывод в обратном порядке -id
    #     return queryset


def delete(request, id):
    try:
        product = Product.objects.get(id=id)  # выбрали запись
        # Deleting files

        os.remove(f"media/{str(product.images)}")  # Удаление файла
        # if str(product.preview_images)[1:]:  # если есть вообще
        # os.remove(f'media/{str(product.preview_images)[1:]}')  # Удаление превьюшки (первый слеш мешал жить)

        product.delete()  # удалили запись
        return HttpResponseRedirect("/")
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Удаление</h2>")


class FilesUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = ("__all__")
    fields = ["quantity", "material", "FinishWork", "Fields"]
    template_name = "product_update_form.html"
    login_url = "login"


class FilesCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["quantity", "material", "FinishWork", "Fields", "images"]

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def price(request):
    price_shirka = Material.objects.filter(
        type_print=1
    )  # Только широкоформатная печать!!!
    price_interierka = Material.objects.filter(
        type_print=2
    )  # Только Интерьерная печать!!!
    price_UV = Material.objects.filter(type_print=3)  # Только UV печать!!!
    finishka = FinishWork.objects.all()  # Только финишка печать!!!
    return render(
        request,
        "price.html",
        {
            "price_shirka": price_shirka,
            "price_interierka": price_interierka,
            "price_UV": price_UV,
            "finishka": finishka,
            "title": "Прайс-листы для Рекламных агентств",
        },
    )


class FileList(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Product
    template_name = "all_files_detail.html"
    login_url = "login"


def add_files_in_base():
    print("где я", os.getcwd())
    os.path.relpath("unzip")
    list_files = os.listdir("unzip")
    # list_files = os.listdir(os.path.relpath('unzip'))
    print(list_files)
    print(os.path.relpath("unzip"))
    return list_files


def upload_arh(request):
    if request.POST:
        form = UploadArhive(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data['path_file'])
            file_name = form.cleaned_data["path_file"]
            # # сюда написать функцию которая убирает пробелы в имени файла
            # arh_name = form.cleaned_data['path_file']
            # path_download = os.path.abspath(str(arh_name))
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
        form = Calculator(request.POST)
        if form.is_valid():
            form = Calculator(request.POST)
            length = request.POST["length"]
            width = request.POST["width"]
            material = request.POST["material"]
            finishka = request.POST["finishka"]
            materials = Material.objects.get(id=material)
            finishkas = FinishWork.objects.get(id=finishka)
            perimetr = (float(width) + float(length)) * 2
            finishka_price = perimetr * finishkas.price
            results = (
                float(width) * float(length) * materials.price
            ) + finishka_price  # в см
            results = round(results, -1)
            return render(
                request,
                "calculator.html",
                {
                    "form": form,
                    "title": "Калькулятор печати для Рекламных агентств",
                    "results": results,
                },
            )

    else:
        form = Calculator()
    return render(
        request,
        "calculator.html",
        {"form": form, "title": "Калькулятор печати для Рекламных агентств"},
    )


class PrintCalculator:
    def __init__(self, length, width, material, finishka):
        pass


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<H1>Страница не найдена</H1")


def view_upload_files_large(request):
    if request.method == "POST":
        form = UploadFilesLarge(request.POST)
        print(request)

        if form.is_valid():
            print(form.cleaned_data)
    form = UploadFilesLarge()
    context = {"form": form}
    return render(request, "files/large_print.html", context)


# class FilesCreateViewInter(LoginRequiredMixin, CreateView):
#     template_name = "files/large_print.html"
#     model = Product
#     form_class = UploadFilesLarge
#     # fields = ["quantity", "material", "FinishWork", "Fields", "images"]
#
#     def form_valid(self, form):
#         form.instance.Contractor = self.request.user
#         return super().form_valid(form)


class FilesCreateViewInter(LoginRequiredMixin, CreateView):
    """Загрузка файлов только для интерьерной печати"""

    model = Product
    form_class = UploadFilesInter
    template_name = "files/inter_print.html"

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)
