#!/bin/bash

### INFO
# Superuser creds --> "admin", "alltagshelfer1234"

#*execute in backend-directory

# Activate virtual environment 
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Delete all migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Uninstall django
pip uninstall Django==4.1.7
# Re-install django
pip install Django==4.1.7

# Set environment variables for settings
export DEBUG=1
export SECRET_KEY='django-insecure-z-gal)z)wg^9d4ktv&bop6+6y$y3j3dw-21c73c@8x!c-pm(kx'
export DJANGO_ALLOWED_HOSTS='* localhost 127.0.0.1 [::1]'

# Make migrations
python manage.py makemigrations users
python manage.py migrate
python manage.py makemigrations
python manage.py migrate

# Load Fixtures
echo '----LOADING FIXTURES---'
# Field Types
python manage.py loaddata fixtures/production/core-fieldtypes.json
### DEV-ONLY ###
# Superuser (Admin)
python manage.py loaddata fixtures/development/users-superuser.json
# Admin Field List Visbility
python manage.py loaddata fixtures/development/users-superuser-userfieldlistvisibility.json
python manage.py loaddata fixtures/development/customers-superuser-customerfieldlistvisibility.json
# Company Sites
python manage.py loaddata fixtures/development/core-companysites.json
# Load Dummy Data
# Users
python manage.py loaddata fixtures/development/users-users.json
# Field Meta Data (Users)
python manage.py loaddata fixtures/development/core-users-fieldmetadata.json
# Field Meta Data (Customers)
python manage.py loaddata fixtures/development/core-customers-fieldmetadata.json
# User Field Values 
python manage.py loaddata fixtures/development/users-userfieldvalues.json
# User Field List Visbility
python manage.py loaddata fixtures/development/users-userfieldlistvisibility.json
# Customers
python manage.py loaddata fixtures/development/customers-customers.json
# Customer Field Values 
python manage.py loaddata fixtures/development/customers-customerfieldvalues.json
# Customer Field List Visibility
python manage.py loaddata fixtures/development/customers-customerfieldlistvisibility.json

# Collect static files
python3 manage.py collectstatic