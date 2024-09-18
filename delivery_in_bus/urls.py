from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrdersForBus, render_instruction, \
    load_img_phone, load_img_number, add_comment, courier_img, complete

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrdersForBus.as_view(), name='orders_for_courier_in_bus'),
    path("instruction/<int:order_id>", render_instruction, name='instruction_for_courier'),
    path("load_img_phone/<int:order_id>", load_img_phone, name='load_img_phone'),
    path("load_img_number/<int:order_id>", load_img_number, name='load_img_number'),

    path("complete/<int:order_id>", complete, name='complete'),

    path("courier_img/<int:order_id>", courier_img, name='courier_img')

]
