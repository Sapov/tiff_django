from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrdersForBus

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrdersForBus.as_view(), name='orders_for_courier_in_bus')

]
