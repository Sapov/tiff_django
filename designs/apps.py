from django.apps import AppConfig


class DesignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designs'

    def ready(self):
        # Импортируем сигналы только после полной загрузки приложения
        from . import signals