# core/models.py

import uuid
from django.db import models
import unidecode
from django.utils.translation import gettext_lazy as _
from core.constants import (Kind, InputTypes, DataTypes,
                            Salutations)
from django.contrib.postgres.fields import ArrayField


class ReturnValuesMixin:
    """
    Mixing for returning all values of instance
    using <Objectname>.objects.get(uuid=uuid).values()
    """

    def values(self):
        return [(field.verbose_name, field.value_from_object(self))
                for field in self.__class__._meta.fields]


class CoreModel(ReturnValuesMixin, models.Model):
    """
    An abstract base class model that provides selfupdating:
    ''author''
    ''created_at''
    ''modified_at''
    """

    class Meta:
        # abstract base class
        abstract = True

    author = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, blank=True,
        null=True, verbose_name=_('Ersteller'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Erstellt am'))
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Bearbeitet am'))


class CoreDataModel(ReturnValuesMixin, models.Model):
    """
    Core Fields for Users and Customers
    """

    class Meta:
        # abstract base class
        abstract = True

    class SalutationChoices(models.TextChoices):
        MR = Salutations.MR, 'Herr'
        MS = Salutations.MS, 'Frau'
        DIVERS = Salutations.DIVERS, 'Divers'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name=_('UUID'))
    salutation = models.CharField(
        max_length=255, choices=SalutationChoices.choices,
        verbose_name=_('Anrede'))
    lastname = models.CharField(max_length=255, verbose_name=_('Name'))
    firstname = models.CharField(max_length=255, verbose_name=_('Vorname'))
    street = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=_('Straße'))
    house_number = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Hausnummer'))
    city = models.CharField(blank=True,
                            null=True, max_length=255, verbose_name=_('Ort'))
    zip = models.CharField(blank=True,
                           null=True, max_length=10, verbose_name=_('PLZ'))
    address_addition = models.CharField(max_length=255, blank=True, null=True,
                                        verbose_name=_('Adresszusatz'))
    phone_mobile = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Mobilnummer'))
    phone_house = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Telefonnummer'))
    birthday = models.DateField(blank=True,
                                null=True, verbose_name=_('Geburstdatum'))
    email = models.EmailField(blank=True, null=True,
                              verbose_name=_('E-Mail'))
    comments = models.TextField(
        blank=True, null=True, verbose_name=_('Notiz'))
    deleted = models.BooleanField(default=False, verbose_name=_('Gelöscht'))
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Gelöscht am'))
    exclude = ['deleted']


class FieldType(ReturnValuesMixin, models.Model):

    class DataTypeChoices(models.TextChoices):
        BOOLEAN = DataTypes.BOOLEAN, 'boolean'
        INT = DataTypes.INT, 'integer'
        FLOAT = DataTypes.FLOAT, 'float'
        STRING = DataTypes.STRING, 'string'
        DATE = DataTypes.DATE, 'date'

    class InputTypeChoices(models.TextChoices):
        MULTISELECT = InputTypes.MULTISELECT, 'multiselect'
        SELECT = InputTypes.SELECT, 'select'
        CHECKBOX = InputTypes.CHECKBOX, 'checkbox'
        INPUT = InputTypes.INPUT, 'input'
        DATE = InputTypes.DATE, 'date'

    data_type = models.CharField(
        max_length=255, choices=DataTypeChoices.choices,
        verbose_name=_('Daten-Typ'))

    input_type = models.CharField(
        max_length=255, choices=InputTypeChoices.choices,
        verbose_name=_('Input-Typ'))

    class Meta:
        verbose_name_plural = _('Feldtypen')
        verbose_name = _('Feldtyp')
        db_table = "field_types"

    def __str__(self):
        return str(self.data_type) + ' - ' + str(self.input_type)


class FieldMetadata(CoreModel):
    """
    Base Model for Custom Fields
    """
    class Meta:
        """
        # Constraints for model
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'kind'], name='unique_title_per_kind'),
            models.UniqueConstraint(
                fields=['position', 'kind'], name='unique_position_per_kind')
        ]
        """
        verbose_name_plural = _('Zusatzfelder Metainformationen')
        verbose_name = _('Zusatzfeld Metainformationen')
        db_table = "field_metadata"
        ordering = ["-created_at"]

    class KindChoices(models.TextChoices):
        USER = Kind.USER, 'Benutzer'
        CUSTOMER = Kind.CUSTOMER, 'Kunde'

    name = models.CharField(max_length=255, blank=True,
                            null=True,
                            verbose_name=_('Technische Bezeichnung'))
    title = models.CharField(
        max_length=255, verbose_name=_('Titel'))
    field_type = models.ForeignKey("FieldType", on_delete=models.CASCADE,
                                   verbose_name=_('Feldtyp'))
    # enums = models.CharField(max_length=500, null=True,
    #                          blank=True, verbose_name=_('Werteliste'))
    enums = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        verbose_name=_('Werteliste')
    )
    required = models.BooleanField(
        default=False, verbose_name=_('Erforderlich'))
    placeholder = models.CharField(
        max_length=500, null=True, blank=True, verbose_name=_('Placeholder'))
    position = models.IntegerField(null=True, verbose_name=_('Position'))
    kind = models.CharField(max_length=255, choices=KindChoices.choices,
                            verbose_name=_(
                                'Typen-Zugehörigkeit'))
    default_visible = models.BooleanField(
        default=False, verbose_name=_('Standardmäßig sichtbar'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Set name (technical) of FieldMetadata
        self.name = unidecode.unidecode(self.title).lower()
        super(FieldMetadata, self).save(*args, **kwargs)


class CompanySite(models.Model):

    class Meta:
        verbose_name_plural = _('Standorte')
        verbose_name = _('Standort')
        db_table = "companysites"

    street = models.CharField(
        max_length=500, verbose_name=_('Straße'))
    house_number = models.CharField(
        max_length=255, verbose_name=_('Hausnummer'))
    city = models.CharField(max_length=255, verbose_name=_('Ort'))
    zip = models.CharField(max_length=10, blank=True,
                           null=True, verbose_name=_('PLZ'))
    address_addition = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Wegbeschreibung'))
    phone = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('Telefonnummer'))
    comments = models.TextField(blank=True, null=True, verbose_name=_('Notiz'))

    def __str__(self):
        # Return primary key
        return str(self.id)
        # return self.city + ' (' + self.street + ' ' + self.house_number + ')'
