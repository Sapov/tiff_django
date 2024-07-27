from django.contrib import admin
from .models import Profile, Delivery, DeliveryAddress


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
    raw_id_fields = ['user']


admin.site.register(Delivery)
admin.site.register(DeliveryAddress)
