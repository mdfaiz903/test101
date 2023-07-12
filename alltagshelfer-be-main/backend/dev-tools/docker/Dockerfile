FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN groupadd -r djangousers && useradd -g djangousers djangomaster

RUN pip3 install psycopg2-binary
RUN pip3 install django-colorfield
COPY ../../ /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
USER djangomaster
CMD python3 manage.py migrate && gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 alltagshelfer_be.wsgi:application
