# Deployment


## Migration

Since this project uses a custom user model, the user model has to be migrated first, before all the other components.

1. <code>python manage.py makemigrations users</code><br>
2. <code>python manage.py migrate</code><br>
3. <code>python manage.py makemigrations</code><br>
4. <code>python manage.py migrate</code><br>