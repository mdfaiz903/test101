# customers/models.py
import datetime
from django.db import models
from core.models import (CoreModel, CoreDataModel, FieldMetadata,
                         CompanySite, ReturnValuesMixin)
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class Customer(CoreModel, CoreDataModel):
    """
    Customer Model
    """

    custom_fields = models.ManyToManyField(
        FieldMetadata,
        through='CustomerFieldValue',
        through_fields=('customer', 'field'),
        verbose_name=_('Benutzerdefinierte Felder für Kunden'))

    def __str__(self):
        return str(self.firstname) + ' ' + str(self.lastname)

    class Meta:
        verbose_name_plural = _('Kunden')
        verbose_name = _('Kunde')
        db_table = "customers"
        ordering = ["-created_at"]

    def get_custom_field_values(self):
        """
        Method to return all assigned custom field values for this customer.
        :return: A list of custom field value objects belonging to the customer.
        """
        return self.custom_fields.through.objects.filter(customer=self).all()

    def delete(self):
        self.deleted = True
        self.deleted_at = make_aware(datetime.datetime.now())
        self.save()
        return True


class CustomerFieldValue(models.Model):
    """
    Model for Custom Customer Field Values
    """

    field = models.ForeignKey(
        FieldMetadata, on_delete=models.CASCADE, verbose_name=_('Feld'))
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name=_('Mitarbeiter'))
    """
    value = models.CharField(max_length=500, verbose_name=_('Wert'))
    """
    value = ArrayField(
        models.CharField(max_length=500, null=True, blank=True,),
        null=True,
        blank=True,
        verbose_name=_('Wert')
    )

    def __str__(self):
        return str(self.field.title)

    class Meta:
        db_table = "customer_fields_values"
        verbose_name_plural = _('Benutzerdefinierte Felder')
        verbose_name = _('Benutzerdefiniertes Feld')


class CustomerFieldListVisibility(ReturnValuesMixin, models.Model):
    """
    Model for visibility settings (in list) of fields per user
    """
    fieldname = models.CharField(max_length=255, verbose_name=_('Feld'))
    visible = models.BooleanField(default=False, verbose_name=_('Sichtbar'))
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name=_('Benutzer'))

    def __str__(self):
        return str(self.fieldname)

    class Meta:
        db_table = "customer_fields_visbility"
        verbose_name_plural = _('Sichtbarkeit der Kundenfelder in Übersicht')
        verbose_name = _('Sichtbarkeit der Kundenfelder in Übersicht')
