from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from .views import *

app_name = 'info'

urlpatterns = [
    path('', banner, name='banner'),
    path('banner/', index, name='ba'),
    path('help/', help_info, name='help'),
    path('finishing_work/', finishing, name='finishing_work'),

]
