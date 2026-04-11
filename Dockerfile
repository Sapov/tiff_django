FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Создаем директории
RUN mkdir -p /django/{media/{image,orders,arhive},static}

WORKDIR /django

# Копируем зависимости
COPY pyproject.toml ./

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir django gunicorn psycopg2-binary redis celery flower

# Если в pyproject.toml есть другие зависимости, установите их
RUN pip install --no-cache-dir -e . || true

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -rms /bin/bash django && \
    chown -R django:django /django

USER django

CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]