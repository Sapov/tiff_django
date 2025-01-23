from django.contrib import admin
from django.urls import path, include

from .views import AddLids, DetailLids, ListLids

app_name = "lids"

urlpatterns = [
    path("add_lids/", AddLids.as_view(), name="add_lids"),
    path("detail_lid/<pk>", DetailLids.as_view(), name="detail_lid"),
    path('listlids/', ListLids.as_view(), name='listlids')
]
