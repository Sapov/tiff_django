from django.contrib import admin
from .models import Order, OrderItem, StatusOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Order._meta.fields]
    list_display = ['id', 'total_price', 'organisation_payer', 'paid', 'status', 'created', 'date_complete']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['paid', 'status']

    inlines = [OrderItemInline]


admin.site.register(StatusOrder)


class StatusOrderAdmin(admin.ModelAdmin):
    model = StatusOrder
    raw_id_fields = ['name']



admin.site.register(OrderItem)
