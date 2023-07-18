from django.contrib import admin
from django.urls import path
from .views import OrderCreateView, OrderItemCreateView, view_order, View_order_item, all_files_in_order, \
    OrderUpdateView, DeleteOrderView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name="create_order"),
    path('create/<pk>', OrderUpdateView.as_view(), name="update_order"),
    path('createitem/', OrderItemCreateView.as_view(), name="create_itmorder"),
    path('view_order/', view_order, name="view_order"),
    path('view_order_item/<pk>', View_order_item.as_view(), name="view_order_items"),
    path('delete_order/<pk>', DeleteOrderView.as_view(), name="Delete_order"),
    path('all_files_in_order/<int:order_id>', all_files_in_order, name="all_files_in_order"),
    # path('all_files_in_order/<int:order_id>/delete', DeleteOrderView.as_view(), name="Delete_order"),

    # path('files/', FilesCreate.as_view())

]
