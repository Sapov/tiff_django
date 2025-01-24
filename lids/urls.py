from django.contrib import admin
from django.urls import path, include

from .views import AddLids, DetailLids, ListLids, UpdateLids, DeleteLids, UpdateStatus

app_name = "lids"

urlpatterns = [
    path("add_lids/", AddLids.as_view(), name="add_lids"),
    path("detail_lid/<pk>", DetailLids.as_view(), name="detail_lid"),
    path('list_lids/', ListLids.as_view(), name='list_lids'),
    path('edit_lids/<pk>', UpdateLids.as_view(), name='edit_lids'),
    path('delete_lids/<pk>', DeleteLids.as_view(), name='delete_lids'),
    path('update_status/<pk>', UpdateStatus.as_view(), name='update_status'),
]
