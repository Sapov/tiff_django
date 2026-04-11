FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/django:/usr/local/lib/python3.10/site-packages"

EXPOSE 8000

# Обновляем pip и устанавливаем системные зависимости
RUN pip install --upgrade pip && \
    apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Создаем директории
RUN mkdir -p /django/{media/{image,orders,arhive},static}

WORKDIR /django

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock* ./

# Устанавливаем зависимости
ENV UV_VIRTUALENVS_CREATE=0
RUN if [ -f uv.lock ]; then \
        uv sync --no-dev; \
    else \
        uv pip install --system -e .; \
    fi

# Проверяем установку Django
RUN python -c "import django; print(f'Django {django.get_version()} installed')"

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -rms /bin/bash django && \
    chown -R django:django /django

USER django

# Запуск
CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]