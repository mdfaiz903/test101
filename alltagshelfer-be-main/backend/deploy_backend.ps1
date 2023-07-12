### INFO
# Superuser creds --> "admin", "alltagshelfer1234"
$env:DJANGO_ALLOWED_HOSTS = 'localhost'
$env:SECRET_KEY = 'mysecretkey'
$env:DEBUG = 1
$env:DB_PASSWORD = 'test123'
$env:DB_USER = 'eugen'

$exclude = @('__init__.py')
Get-ChildItem -Path ".\core\migrations\" -Exclude $exclude  | Remove-Item -Recurse
Get-ChildItem -Path ".\users\migrations\" -Exclude $exclude  | Remove-Item -Recurse
Get-ChildItem -Path ".\customers\migrations\" -Exclude $exclude  | Remove-Item -Recurse
Get-ChildItem -Path ".\appointments\migrations\" -Exclude $exclude  | Remove-Item -Recurse
Get-ChildItem -Path ".\services\migrations\" -Exclude $exclude  | Remove-Item -Recurse
Get-ChildItem -Path ".\api\migrations\" -Exclude $exclude  | Remove-Item -Recurse
$env:DB_PASSWORD = 'test123'
$env:DB_USER = 'eugen'
# Make migrations
python manage.py makemigrations users
# python manage.py migrate
python manage.py makemigrations
# python manage.py migrate

# Create superuser
#$env:DJANGO_SUPERUSER_USERNAME = 'test'
#$env:DJANGO_SUPERUSER_FIRSTNAME = 'admin_firstname'
#$env:DJANGO_SUPERUSER_LASTNAME = 'admin_lastname'
#$env:DJANGO_SUPERUSER_PASSWORD = 'test123'
#python manage.py createsuperuser --no-input

