# appointments/models.py

import uuid
import calendar
import datetime
from django.db import models
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from core.models import (CoreModel, ReturnValuesMixin)
from core.constants import (Frequencies, Weekdays)
from users.models import User


class Appointment(ReturnValuesMixin, models.Model):
    """
    Appointment Model
    """

    id = models.UUIDField(primary_key=True, default=uuid. uuid4 , editable=False, verbose_name=_('UUID'))
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name=_('Author'), related_name='appointmentauthor')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name=_('Mitarbeiter'), related_name='employee')
    customer = models.ForeignKey("customers.Customer", on_delete=models.SET_NULL,null=True, verbose_name=_('Kunde'))
    service = models.ForeignKey("services.Service", on_delete=models.SET_NULL,blank=True, null=True, verbose_name=_('Leistung'))
    series = models.ForeignKey("appointments.AppointmentSeries", on_delete=models.SET_NULL,null=True, verbose_name=_('Serientermin'))
    start_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Startzeitpunkt'))
    end_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Endzeitpunkt'))
    comments = models.TextField(blank=True, null=True, verbose_name=_('Kommentar'))
    deleted = models.BooleanField(default=False, verbose_name=_('Gelöscht'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Gelöscht am'))

    class Meta:
        verbose_name_plural = _('Termine')
        verbose_name = _('Termin')
        db_table = "appointments"
        ordering = ["-end_datetime"]

    def delete(self):
        self.deleted = True
        self.deleted_at = make_aware(datetime.datetime.now())
        self.save()
        return True


class AppointmentSeries(ReturnValuesMixin, models.Model):
    """
    Appointment Series Model
    """

    class FrequencyChoices(models.TextChoices):
        DAIlY = Frequencies.DAIlY, 'Täglich'
        WEEKLY = Frequencies.WEEKLY, 'Wöchentlich'
        BIWEEKLY = Frequencies.BIWEEKLY, '2-Wöchentlich'
        MONTHLY = Frequencies.MONTHLY, 'Monatlich'
        BIMONTHLY = Frequencies.BIMONTHLY, '2-Monatlich'
        QUATERLY = Frequencies.QUATERLY, 'Vierteljährlich'
        HALFYEARLY = Frequencies.HALFYEARLY, 'Halbjährlich'
        YEARLY = Frequencies.YEARLY, 'Jährlich'

    class WeekdayChoices(models.TextChoices):
        MONDAY = Weekdays.MONDAY, 'Montag'
        TUESDAY = Weekdays.TUESDAY, 'Dienstag'
        WEDNESDAY = Weekdays.WEDNESDAY, 'Mittwoch'
        THURSDAY = Weekdays.THURSDAY, 'Donnerstag'
        FRIDAY = Weekdays.FRIDAY, 'Freitag'
        SATURDAY = Weekdays.SATURDAY, 'Samstag'
        SUNDAY = Weekdays.SUNDAY, 'Sonntag'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name=_('UUID'))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('Author'), related_name='appointmentseriesauthor')
    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.SET_NULL,
        null=True, verbose_name=_('Kunde')
    )
    start_date = models.DateField(verbose_name=_('Startdatum'))
    end_date = models.DateField(verbose_name=_('Enddatum'))
    start_time = models.TimeField(verbose_name=_('Start-Uhrzeit'))
    end_time = models.TimeField(verbose_name=_('End-Uhrzeit'))
    weekdays = ArrayField(
        models.CharField(max_length=32, blank=True,
                         choices=WeekdayChoices.choices),
        default=list, verbose_name=_('Wochentage')
    )
    frequency = models.CharField(
        max_length=255, choices=FrequencyChoices.choices,
        verbose_name=_('Häufigkeit'))
    deleted = models.BooleanField(default=False, verbose_name=_('Gelöscht'))
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Gelöscht am'))

    class Meta:
        verbose_name_plural = _('Serientermine')
        verbose_name = _('Serientermin')
        db_table = "appointmentsseries"
        ordering = ["-end_date"]

    def delete(self):
        self.deleted = True
        self.deleted_at = make_aware(datetime.datetime.now())
        self.save()
        return True
