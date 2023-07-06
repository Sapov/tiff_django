from django.contrib import admin
from django.urls import path, include
from .views import index, delete, FilesUpdateView, FilesCreateView, price, FileList, add_files_SHIRKA

app_name = 'files'

urlpatterns = [
    path('', index, name='home'),
    path('files_dl/', FileList.as_view(), name='files'),
    path('create/', FilesCreateView.as_view(), name="create_files"),  # форма добавления файла
    path('edit/<pk>', FilesUpdateView.as_view(), name="update_files"),  # форма редактирования файла
    path('delete/<int:id>/', delete),
    path('price/', price),
    path('add_files/', add_files_SHIRKA, name ='add_file1'),

    # path('files/', FilesCreate.as_view())

]
