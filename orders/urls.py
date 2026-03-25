from django.contrib import admin
from django.urls import path
from .views import (
    View_order_item,
    OrderUpdateView,
    DeleteOrderView,
    add_files_in_order,
    add_item_in_order,
    del_item_in_order,
    order_pay,
    view_all_files_for_work_in_orders,
    ViewAllPayOrders,
    report_complete_orders,
    new_order,
    OrdersViewList,
    AllOrdersListView, report_day, create_invoice, web_hook, fail_payment, success_payment,
    get_invoice, create_pay_link,
)
from files.views import about_file

app_name = "orders"

urlpatterns = [
    path("neworder/", new_order, name="new_order"),  # Добавить новый заказ
    path(
        "create/<pk>", OrderUpdateView.as_view(), name="update_order"),
    # Редактировать заказ
    path("view_orders/", OrdersViewList.as_view(), name="view_orders"),  # посмотреть мои заказы
    path("view_order_item/<pk>", View_order_item.as_view(), name="view_order_items"),
    path("delete_order/<pk>", DeleteOrderView.as_view(), name="Delete_order"),
    path("add_files_in_order/<int:order_id>", add_files_in_order, name="add_file_in_order", ),
    path("add_item_in_order/<int:order_id>/<int:item_id>", add_item_in_order, name="add"),
    path("del_item_in_order/<int:order_id>/<int:item_id>/<int:item_product_id>", del_item_in_order,
         name="del_item_in_order", ),

    # Посмотреть все заказы
    path("view_all_orders/", AllOrdersListView.as_view(), name="view_all_orders"),
    path("view_all_orders_pay/", ViewAllPayOrders.as_view(), name="view_all_orders_pay"),  # все оплаченые заказы
    path("view_all_files_for_work_in_orders/", view_all_files_for_work_in_orders,
         name="view_all_files_for_work_in_orders", ),  # все файлы в работе
    path("order_pay/<int:order_id>", order_pay, name="order_pay"),
    # --------отчеты
    path('report_day/', report_day, name='report_day'),
    path("report/", report_complete_orders, name="report_complete_orders"),

    # BANK
    path('web_hook/', web_hook, name='web_hook'),
    path('fail/', fail_payment, name='fail_payment'),
    path('success/', success_payment, name='success_payment'),

    # Invoice
    path('get_invoice/<int:order_id>', get_invoice, name='get_invoice'),
    path('create_invoice/<int:order_id>', create_invoice, name='create_invoice'), # скачать счет
    path('create_pay_link/<int:order_id>', create_pay_link, name='create_pay_link'), # Генерируем ссылку

]


