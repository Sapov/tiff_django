FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc gettext cron openssh-client locales vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Создаем пользователя
RUN useradd -rms /bin/bash django && \
    mkdir -p /django/{media/{image,orders,arhive},static} && \
    chown -R django:django /django

WORKDIR /django

# Копируем зависимости
COPY --chown=django:django pyproject.toml uv.lock ./

# НЕ отключаем виртуальное окружение (по умолчанию создается .venv)
RUN uv sync --frozen --no-dev && \
    chown -R django:django /django/.venv

# Копируем код
COPY --chown=django:django . .

# Добавляем .venv/bin в PATH (или используем uv run)
ENV PATH="/django/.venv/bin:$PATH"

USER django

# Вариант 1: через PATH
CMD ["bash", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 mysite.wsgi:application"]

# ИЛИ вариант 2: через uv run
# CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:8000", "mysite.wsgi:application"]