from django.contrib import admin
from django.urls import path
from .views import OrderCreateView, OrderItemCreateView, view_order, View_order_item, \
    OrderUpdateView, DeleteOrderView, add_files_in_order, add_item_in_order, del_item_in_order, order_pay, \
    view_all_orders, view_all_files_for_work_in_orders, ViewAllPayOrders

app_name = 'orders'

urlpatterns = [
    path('new_order/', OrderCreateView.as_view(), name="new_order"), # Добавть новый зааказ
    # path('new_order1/', new_order, name="new_order"), # Добавть новый зааказ
    path('create/<pk>', OrderUpdateView.as_view(), name="update_order"), # Редактировать заказ
    path('createitem/', OrderItemCreateView.as_view(), name="create_itmorder"),
    path('view_orders/', view_order, name="view_orders"), # посмотерть мои заказы
    path('view_order_item/<pk>', View_order_item.as_view(), name="view_order_items"),
    path('delete_order/<pk>', DeleteOrderView.as_view(), name="Delete_order"),

    path('add_files_in_order/<int:order_id>', add_files_in_order, name="add_file_in_order"),
    path('add_item_in_order/<int:order_id>/<int:item_id>', add_item_in_order, name="add"),
    path('del_item_in_order/<int:order_id>/<int:item_id>', del_item_in_order, name="del_item_in_order"),
    path('view_all_orders/', view_all_orders, name="view_all_orders"), # все оплаченые заказы

    path('view_all_orders_pay/', ViewAllPayOrders.as_view(), name="view_all_orders_pay"), # все оплаченые заказы
    path('view_all_files_for_work_in_orders/', view_all_files_for_work_in_orders, name="view_all_files_for_work_in_orders"), # все файлы в работе
    path('order_pay/<int:order_id>', order_pay, name="order_pay"),
    # path('add/<product_id>/', addin, name="add"),
    # path('files/', FilesCreate.as_view())

]
