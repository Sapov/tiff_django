from django.contrib import admin
from django.urls import path, include

from .forms import UploadFilesInter
from .pay import check_signature_result, success_pay, fail
from .views import (
    index,
    delete,
    FilesUpdateView,
    FilesCreateView,
    price,
    FileList,
    upload_arh,
    calculator,
    ViewFilesUserListView,
    FilesCreateViewInter,
    FilesCreateViewLarge,
    FilesCreateViewUV,
    FilesCreateViewRollUp,
)

app_name = "files"

urlpatterns = [
    path("", index, name="myfiles"),  # Myfiles
    path("ind/", ViewFilesUserListView.as_view(), name="myfiles1"),  # Myfiles
    path("allfiles/", FileList.as_view(), name="all_files"),
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
    path("calculator/", calculator, name="calculator"),  # Calculator

    # https://docs.robokassa.ru/pay-interface/#notification
    path("result/", check_signature_result, name="result"),  # для робокассы проверкаe
    path("success/", success_pay, name="success_pay"),  # заказ успешно оплачен
    path("success/", fail, name="fail_pay"),  # заказ НЕуспешно оплачен
]
