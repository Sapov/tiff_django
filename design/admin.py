from django.contrib import admin
from .models import OrdDesign, Comment


class OrderDesignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'description')


admin.site.register(OrdDesign, OrderDesignAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'article__title')
