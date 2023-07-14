#FROM python:3.10-alpine
#WORKDIR /django
#COPY .. /django
#RUN apk update && pip install -r /django/requirements.txt --no-cache-dir
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#
#FROM python:3.10.9
#
#SHELL ["/bin/bash", "-c"]
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN pip install --upgrade pip
#
#RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
#    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim
#
#RUN useradd -rms /bin/bash yt && chmod 777 /opt /run
#
#WORKDIR /yt
#
#RUN mkdir /yt/static && mkdir /yt/media && chown -R yt:yt /yt && chmod 755 /yt
#
#COPY --chown=yt:yt . .
#
#RUN pip install -r requirements.txt
#
#USER yt
#
#CMD ["gunicorn","-b","0.0.0.0:8001","soaqaz.wsgi:application"]


# Используем официальный образ Python в качестве базового образа
FROM python:3.10-alpine
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code
RUN mkdir /code/static && mkdir /code/media && mkdir /code/media/image && mkdir /code/media/preview

# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt ./
# Устанавливаем зависимости, описанные в файле requirements.txt
RUN pip install -r requirements.txt