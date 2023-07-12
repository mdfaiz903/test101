# api/admin.py

from django.contrib import admin
from .models import BlacklistedToken


class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ['expiration_datetime', 'token']


admin.site.register(BlacklistedToken, BlacklistedTokenAdmin)
