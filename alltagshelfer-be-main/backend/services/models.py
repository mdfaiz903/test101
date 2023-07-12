# services/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from core.models import CoreModel


class Service(CoreModel):
    """
    Services Model
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_('Bezeichnung'))
    calendar_color = ColorField(
        default='#FF0000', verbose_name=_('Kalenderfarbe'))
    hourly_rate = models.FloatField(
        blank=True, null=True, verbose_name=_('Stundenpreis'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('Beschreibung'))

    class Meta:
        verbose_name_plural = _('Leistungen')
        verbose_name = _('Leistung')
        db_table = "services"
        ordering = ["-created_at"]
