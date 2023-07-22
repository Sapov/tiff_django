from django.contrib import admin
from django.urls import path
from .views import OrderCreateView, OrderItemCreateView, view_order, View_order_item, all_files_in_order, \
    OrderUpdateView, DeleteOrderView, add_files_in_order, order_pay

app_name = 'orders'

urlpatterns = [
    path('new_order/', OrderCreateView.as_view(), name="new_order"),
    path('create/<pk>', OrderUpdateView.as_view(), name="update_order"),
    path('createitem/', OrderItemCreateView.as_view(), name="create_itmorder"),
    path('view_orders/', view_order, name="view_orders"), # посмотерть мои заказы
    path('view_order_item/<pk>', View_order_item.as_view(), name="view_order_items"),
    path('delete_order/<pk>', DeleteOrderView.as_view(), name="Delete_order"),
    path('add_files_in_order/<int:order_id>', add_files_in_order, name="Add_file_in_order"),
    path('all_files_in_order/<int:order_id>', all_files_in_order, name="all_files_in_order"),
    path('order_pay/<int:order_id>', order_pay, name="order_pay"),
    # path('add/<product_id>/', addin, name="add"),

    # path('files/', FilesCreate.as_view())

]
