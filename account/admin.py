from django.contrib import admin
from .models import Delivery, DeliveryAddress

admin.site.register(Delivery)
admin.site.register(DeliveryAddress)
