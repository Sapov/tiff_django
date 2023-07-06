from django.contrib import admin
from .models import Order, OrderItem, StatusOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(StatusOrder)

class StatusOrderAdmin(admin.ModelAdmin):
    model = StatusOrder
    raw_id_fields = ['name']
