from django.contrib import admin
from django.urls import path
from .views import (
    view_order,
    View_order_item,
    OrderUpdateView,
    DeleteOrderView,
    add_files_in_order,
    add_item_in_order,
    del_item_in_order,
    order_pay,
    view_all_files_for_work_in_orders,
    ViewAllPayOrders,
    about_file,
    report_complete_orders,
    new_order,
    OrdersViewList,
    AllOrdersListView, result, success_pay, fail, report_day, create_invoice, web_hook
)

app_name = "orders"

urlpatterns = [
    # path('new_order/', OrderCreateView.as_view(), name="new_order"), # Добавить новый заказ
    path("neworder/", new_order, name="new_order"),  # Добавить новый заказ
    path(
        "create/<pk>", OrderUpdateView.as_view(), name="update_order"),
    # Редактировать заказ
    path("view_orders/", view_order, name="view_orders"),  # посмотреть мои заказы
    path("view_orders1/", OrdersViewList.as_view(), name="view_orders1"),  # посмотреть мои заказы
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
    path("about_file/<int:file_id>", about_file, name="about_file"),
    # --------отчеты
    path('report_day/', report_day, name='report_day'),
    path("report/", report_complete_orders, name="report_complete_orders"),

    # https://docs.robokassa.ru/pay-interface/#notification
    path("result/", result, name="result"),  # для робокассы проверкаe
    path("success/", success_pay, name="success_pay"),  # заказ успешно оплачен
    path("fail/", fail, name="fail_pay"),  # заказ НЕуспешно оплачен
    # BANK
    path('create_invoice/<int:order_id>', create_invoice, name='create_invoice'),
    # path('create_web_hook/', create_web_hook, name='create_web_hook',)
    path('web_hook/', web_hook, name='web_hook',)
]
