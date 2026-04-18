FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /django

# Копируем зависимости
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -e . || true
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -rms /bin/bash django && \
    chown -R django:django /django

# Создаем директории ПОСЛЕ смены владельца
RUN mkdir -p /django/media/image /django/media/orders /django/media/arhive  /django/static && \
    chown -R django:django /django

# Переключаемся на пользователя django
USER django

# Запускаем collectstatic от django пользователя
CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]