# validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

def validate_tiff_file(value):
    ext = os.path.splitext(value.name)[1]  # Получаем расширение файла
    valid_extensions = ['.tif', '.tiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('Поддерживаются только TIFF файлы с расширениями .tif или .tiff')
        )