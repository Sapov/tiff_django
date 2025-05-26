from django.contrib import admin
from .models import OrdDesign


class OrderDesignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(OrdDesign, OrderDesignAdmin)

# Register your models here.
