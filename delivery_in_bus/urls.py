from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrdersForBus, render_instruction, \
    load_img_production, load_img_phone

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrdersForBus.as_view(), name='orders_for_courier_in_bus'),
    path("instruction/<int:order_id>", render_instruction, name='instruction_for_courier'),
    path("load_img/<int:order_id>", load_img_production, name='load_img'),
    path("load_img_phone/<int:order_id>", load_img_phone, name='load_img_phone')

]
