FROM python:3.10-slim


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2 \
    && pip3 install psycopg2-binary 
# && groupadd -r djangousers && useradd -g djangousers djangoinit

WORKDIR /app
COPY ../../ /app/
RUN pip3 install django-colorfield
RUN pip3 install -r requirements.txt 
# USER djangoinit
CMD bash -c "./dev-tools/docker/make_dev_migrations.sh && ./dev-tools/docker/db_fixtures.sh"