#!/bin/bash

#*execute in backend-directory

source env/bin/activate

export DEBUG=1
export SECRET_KEY='django-insecure-z-gal)z)wg^9d4ktv&bop6+6y$y3j3dw-21c73c@8x!c-pm(kx'
export DJANGO_ALLOWED_HOSTS='* localhost 127.0.0.1 [::1]'
export DB_PASSWORD='alltagshelfer123'
export DB_USER='alltagshelfer_db_user'

# Core data
# python manage.py dumpdata core > fixtures/core.json
# Core FieldMetaData
# python manage.py dumpdata core > fixtures/core-fieldmetadata.json
# Users
# python manage.py dumpdata users > fixtures/users-users.json
python manage.py dumpdata customers > fixtures/customers-customers.json