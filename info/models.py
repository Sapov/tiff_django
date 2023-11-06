from django.db import models


class Info(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField()
    photo = models.ImageField(upload_to='static_photo/')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    categories = models.CharField(max_length=48)

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"

    def __str__(self):
        return self.categories


class Menu(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, verbose_name='Название страницы')

    def __str__(self):
        return self.title
