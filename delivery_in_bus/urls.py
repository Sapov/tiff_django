from django.urls import path, include

from delivery_in_bus.views import ViewAllCompleteOrders

app_name = 'delivery_in_bus'

urlpatterns = [
    # для Курьеров
    path("courier/", ViewAllCompleteOrders.as_view(), name='orders_for_courier_in_bus')

]
