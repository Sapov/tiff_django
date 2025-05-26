from django.contrib import admin
from .models import OrdDesign, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class OrderDesignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'description')
    inlines = [
        CommentInline,
    ]


admin.site.register(OrdDesign, OrderDesignAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('design', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'article__title')
