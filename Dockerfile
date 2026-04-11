FROM python:3.10.4

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/django/.venv/bin:$PATH"

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Создаем пользователя и директории
RUN useradd -rms /bin/bash django && \
    mkdir -p /django/media/image /django/media/orders /django/media/arhive /django/static && \
    chown -R django:django /django && \
    chmod -R 755 /django

WORKDIR /django

# Копируем ТОЛЬКО файлы с зависимостями (для кэширования)
COPY --chown=django:django pyproject.toml uv.lock ./

# Устанавливаем зависимости от root, но с указанием прав
RUN uv sync --frozen --no-dev && \
    chown -R django:django /django/.venv

# Копируем остальной код (этот слой будет пересобираться часто)
COPY --chown=django:django . .

USER django

# Собираем статику и запускаем gunicorn
CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]