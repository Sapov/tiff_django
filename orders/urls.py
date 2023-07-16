from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('', OrderItemCreateView.as_view(), name="create_files"),

    # path('files/', FilesCreate.as_view())

]
