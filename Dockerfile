# СТЕЙДЖ 1: Генерация requirements.txt
FROM ghcr.io/astral-sh/uv:latest AS uv

COPY pyproject.toml uv.lock* /app/
WORKDIR /app
RUN if [ -f uv.lock ]; then uv export --frozen --no-dev --no-hashes -o requirements.txt; else echo "django==4.2.0" > requirements.txt; fi

# СТЕЙДЖ 2: Основной образ
FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt из первого стейджа
COPY --from=uv /app/requirements.txt /tmp/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Создаем директории
RUN mkdir -p /django/{media/{image,orders,arhive},static}

WORKDIR /django

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -rms /bin/bash django && \
    chown -R django:django /django

USER django

CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]