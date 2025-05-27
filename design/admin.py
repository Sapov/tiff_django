from django.contrib import admin
from .models import OrderDesign, Comments


class CommentInline(admin.TabularInline):
    model = Comments


class OrderDesignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'description')
    inlines = [
        CommentInline,
    ]


admin.site.register(OrderDesign, OrderDesignAdmin)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('designs', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'article__title')
