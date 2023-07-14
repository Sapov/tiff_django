from django.contrib import admin
from django.urls import path, include
from .views import *
from .forms import *

app_name = 'orders'

urlpatterns = [
    path('', add_order),

    # path('add_files/', add_files_SHIRKA, name ='add_file1'),

    # path('files/', FilesCreate.as_view())

]
