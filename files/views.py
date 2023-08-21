import os
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from orders.models import OrderItem
from .models import Product, Material, FinishWork
from .forms import AddFiles, UploadArhive
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin  # new
import patoolib

from .tiff_file import WorkZip


# from django.core.files.storage import FileSystemStorage
@login_required
def index(request):
    '''Вывод файлов толоко авторизованного пользователя'''
    products = Product.objects.filter(Contractor=request.user).order_by('-id')  # вывод в обратном порядке -id
    return render(request, "index.html", {"products": products, 'title': 'Ваши файлоы'})


def delete(request, id):
    try:
        product = Product.objects.get(id=id)  # выбрали запись
        # Deleting files

        os.remove(f'media/{str(product.images)}')  # Удаление файла
        # if str(product.preview_images)[1:]:  # если есть вообще
        # os.remove(f'media/{str(product.preview_images)[1:]}')  # Удаление превьюшки (первый слеш мешал жить)

        product.delete()  # удалили запись
        return HttpResponseRedirect("/")
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Удаление</h2>")


class FilesUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = ("__all__")
    fields = ['quantity', 'material', 'FinishWork', 'Fields']
    template_name = 'product_update_form.html'
    login_url = 'login'


class FilesCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['quantity', 'material', 'FinishWork', 'Fields', 'images']

    def form_valid(self, form):
        form.instance.Contractor = self.request.user
        return super().form_valid(form)


@login_required
def price(request):
    price_shirka = Material.objects.filter(type_print=1)  # Только широкоформатная печать!!!
    price_interierka = Material.objects.filter(type_print=2)  # Только Интерьерная печать!!!
    price_UV = Material.objects.filter(type_print=3)  # Только UV печать!!!
    finishka = FinishWork.objects.all()  # Только финишка печать!!!
    return render(request, "price.html",
                  {"price_shirka": price_shirka, "price_interierka": price_interierka, "price_UV": price_UV,
                   'finishka': finishka, 'title': 'Прайс-листы для Рекламных агентств'})


class FileList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'all_files_detail.html'
    login_url = 'login'


def add_files_in_base():
    print("где я" , os.getcwd())
    os.path.relpath('unzip')
    list_files = os.listdir('unzip')
    # list_files = os.listdir(os.path.relpath('unzip'))
    print(list_files)
    print(os.path.relpath('unzip'))
    return list_files


def upload_arh(request):
    if request.POST:
        form = UploadArhive(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data['path_file'])
            file_name = form.cleaned_data['path_file']
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

    return render(request, 'files/upload_arh.html',
                  {'form': form, 'title': 'Добавление файлов'})  # изменение данных в БД


