FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /django

# Создаем пользователя ДО копирования файлов
RUN useradd -rms /bin/bash django

# Копируем только зависимости (это меняется редко)
COPY pyproject.toml uv.lock requirements.txt ./

# Устанавливаем зависимости (от root)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код (это меняется часто)
COPY --chown=django:django . .

# Создаем директории для медиа и статики (от root, потом меняем владельца)
RUN mkdir -p /django/media/image /django/media/orders /django/media/arhive /django/static && \
    chown -R django:django /django

# Переключаемся на пользователя django
USER django

CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]

