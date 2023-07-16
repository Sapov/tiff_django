from django.contrib import admin
from django.urls import path
from .views import OrderCreateView, OrderItemCreateView, view_order, View_order_item, all_files_in_order

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name="create_order"),
    path('createitem/', OrderItemCreateView.as_view(), name="create_itmorder"),
    path('view_order/', view_order, name="view_order"),
    path('view_order_item/<pk>', View_order_item.as_view(), name="view_order"),
    path('all_files_in_order/<int:order_id>', all_files_in_order, name="all_files_in_order"),

    # path('files/', FilesCreate.as_view())

]
