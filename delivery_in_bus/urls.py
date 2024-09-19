from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrdersForBus, render_instruction, complete

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrdersForBus.as_view(), name='orders_for_courier_in_bus'),
    path("instruction/<int:order_id>", render_instruction, name='instruction_for_courier'),
    path("complete/<int:order_id>", complete, name='complete'),


]
