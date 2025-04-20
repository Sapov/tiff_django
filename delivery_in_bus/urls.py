from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrdersForBus, render_instruction, complete, \
    ViewAllCompleteDeliversForBus, DeliveryDetailVew

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrdersForBus.as_view(), name='orders_for_courier_in_bus'),
    path("complete_delivers_courier_in_bus/", ViewAllCompleteDeliversForBus.as_view(), name='complete_delivers_courier_in_bus'),
    path("instruction/<int:order_id>", render_instruction, name='instruction_for_courier'),
    path("detail_delivery/<int:pk>", DeliveryDetailVew.as_view(), name='detail_delivery'),
    path("complete/<int:order_id>", complete, name='complete'),


]
