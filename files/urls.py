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
    ViewFilesUserListView,
    FilesCreateViewInter,
    FilesCreateViewLarge,
    FilesCreateViewUV,
    FilesCreateViewRollUp, calculator_large_print_out, calculator_blank_out, calculator_uv_print_out,
    calculator_interier_print_out, ViewContractorListView, ContractorCreateView, ContractorUpdateView,
    ContractorDeleteView, confirm_order_to_work, confirm_order_to_complieted,
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
    # --------------calculators--------------
    # calc outer
    path("calculator/", calculator, name="calculator"),  # Calculator
    # Калькулятор на сайт широкоформатная печать
    path("calculator_large_print_out/", calculator_large_print_out, name="calculator_large_print_out"),
    path("calculator_interier_print_out/", calculator_interier_print_out, name="calculator_interier_print_out"),
    path("calculator_uv_print_out/", calculator_uv_print_out, name="calculator_uv_print_out"),
    path("calculator_blank_out/", calculator_blank_out, name="calculator_blank_out"),
    # CRUD Contractor Подрядчики
    path("contractor_view/", ViewContractorListView.as_view(), name="contractor_view"),
    path("contractor_create/", ContractorCreateView.as_view(), name="contractor_create"),
    path("contractor_update/<pk>", ContractorUpdateView.as_view(), name="contractor_update"),
    path("contractor_delete/<pk>", ContractorDeleteView.as_view(), name="contractor_delete"),
    # подтверждение принятия заказа типографией
    path("confirm_order_to_work/<pk>/<hash_code>/", confirm_order_to_work, name="confirm_order_to_work"),
    # поодтверждение готовности заказа
    path("confirm_order_to_competed/<pk>/<hash_code>/", confirm_order_to_complieted, name="confirm_order_to_completed"),

]
