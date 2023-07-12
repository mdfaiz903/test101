# services/admin.py

from django.contrib import admin
from .models import Service
from core.admin import AutomaticAuthorMixin


class ServiceAdmin(AutomaticAuthorMixin, admin.ModelAdmin):
    list_display = ['name', 'calendar_color', 'hourly_rate']
    list_filter = list_display


admin.site.register(Service, ServiceAdmin)
