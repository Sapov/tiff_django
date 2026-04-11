FROM python:3.10.4

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim

RUN useradd -rms /bin/bash django && chmod 777 /opt /run

WORKDIR /django
RUN mkdir /django/media
RUN mkdir /django/media/image
RUN mkdir /django/static && mkdir /django/media/orders  && mkdir /django/media/arhive && chown -R django:django /django && chmod -R 755 /django

COPY --chown=django:django . .

////


# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /django

# Копируем файлы с зависимостями
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-dev

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"


USER django
CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]