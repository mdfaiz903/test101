# appointments/admin.py

from django.contrib import admin
from .models import Appointment, AppointmentSeries
from core.admin import AutomaticAuthorMixin


class AppointmentAdmin(AutomaticAuthorMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'service',
                    'start_datetime', 'end_datetime']
    list_filter = list_display


class AppointmentSeriesAdmin(AutomaticAuthorMixin, admin.ModelAdmin):
    list_display = ['id', 'customer', 'start_date',
                    'end_date', 'frequency']
    list_filter = list_display


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AppointmentSeries, AppointmentSeriesAdmin)
