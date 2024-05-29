from django.contrib import admin
from django.urls import path, include

from .forms import UploadFilesInter
from .views import (
    index,
    delete,
    FilesUpdateView,
    FilesCreateView,
    price,
    upload_arh,
    calculator,
    calculator_large_print,
    ViewFilesUserListView,
    FilesCreateViewInter,
    FilesCreateViewLarge,
    FilesCreateViewUV,
    FilesCreateViewRollUp, calculator_out, calculator_large_print_out,
)

app_name = "files"

urlpatterns = [
    path("", index, name="myfiles"),  # Myfiles
    path("ind/", ViewFilesUserListView.as_view(), name="myfiles1"),  # Myfiles
    # форма добавления файла
    path("create/", FilesCreateView.as_view(), name="create_files"),
    path("create_large/", FilesCreateViewLarge.as_view(), name="create_large"),
    path("create_inter/", FilesCreateViewInter.as_view(), name="create_inter"),
    path("create_uv/", FilesCreateViewUV.as_view(), name="create_uv"),
    path("create_rollup/", FilesCreateViewRollUp.as_view(), name="create_rollup"),
    # форма редактирования файла
    path("edit/<pk>", FilesUpdateView.as_view(), name="update_files"),
    path("delete/<int:id>/", delete),
    path("price/", price, name="price"),  # прайс-лист
    path("upload/", upload_arh, name="upload_arh"),  # загрузка архива файла
    # calculators
    # calc outer
    path("calculator/", calculator, name="calculator"),  # Calculator
    path("calculator_large_print/", calculator_large_print, name="calculator_large_print"),  # calculator_large_print
    path("calculator_out/", calculator_out, name="calculator_out"),  # calculator для общего пользования
    #калькулятор на сайт широкоформатная печать
    path("calculator_large_print_out/", calculator_large_print_out, name="calculator_large_print_out"),


]
