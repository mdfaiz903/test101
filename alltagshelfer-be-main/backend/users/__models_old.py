# users/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse
from core.models import CoreDataModel, FieldsMetaInfo, CoreModel, CompanySite
from django.utils.translation import gettext_lazy as _


"""
USERS
"""


class User(CoreDataModel, AbstractUser):
    """
    General User Model
    """

    class Types(models.TextChoices):
        CAREGIVER = "CAREGIVER", 'Alltagshelfer'
        SUPERVISOR = "SUPERVISOR", 'Teamleiter'
        CEO = "CEO", 'Geschäftsführer'
        ADMIN = "ADMIN", 'Admin'

    # User Fields
    type = models.CharField(max_length=50, choices=Types.choices,
                            default=Types.CAREGIVER, verbose_name=_('Benutzer-Typ'))
    companysite = models.ForeignKey(
        CompanySite, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=200, verbose_name=_('Benutzername'))
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='users', blank=True)
    custom_fields = models.ManyToManyField(
        FieldsMetaInfo,
        through='UserFieldValue',
        through_fields=('user', 'field'),
        verbose_name=_('Benutzerdefinierte Felder für Mitarbeiter'))

    # Remove duplicate user-fields (from AbstractUser)
    last_name = None
    first_name = None

    class Meta:
        verbose_name_plural = _('Benutzer')
        verbose_name = _('Benutzer')
        db_table = "users"
        ordering = ["-created_at"]


class UserFieldValue(CoreModel):
    """
    Model for Custom User Field Values
    """

    field = models.ForeignKey(
        FieldsMetaInfo, on_delete=models.CASCADE, verbose_name=_('Feld'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Mitarbeiter'))
    value = models.CharField(max_length=500, verbose_name=_('Wert'))

    def __str__(self):
        return str(self.field.name)

    class Meta:
        db_table = "user_fields_values"
        verbose_name_plural = _('Benutzerdefinierte Felder')
        verbose_name = _('Benutzerdefiniertes Feld')


class CaregiverManager(models.Manager):
    """
    Model-Manager for Caregivers
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CAREGIVER)


class Caregiver(User):
    """
    Proxy User Model for Caregivers (Alltagshelfer)
    """

    # Set Model Manager
    objects = CaregiverManager()

    # Define as Proxy Model (no database entry)
    class Meta:
        proxy = True

    # Override save, so type doesnt need an extra type-specification in the argument
    # Creating a new user is done by: Caregiver.create(name='',...)
    def save(self, *args, **kwargs):
        if not self.pk:
            # If new pk, set User.Type
            self.type = User.Types.CAREGIVER
        return super().save(*args, **kwargs)


class SupervisorManager(models.Manager):
    """
    Model-Manager for Supervisors
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SUPERVISOR)


class Supervisor(User):
    """
    Proxy User Model for Supervisors (Teamleiter)
    """

    # Set Model Manager
    objects = SupervisorManager()

    # Define as Proxy Model (no database entry)
    class Meta:
        proxy = True

    # Override save, so type doesnt need an extra type-specification in the argument
    # Creating a new user is done by: Supervisor.create(name='',...)
    def save(self, *args, **kwargs):
        if not self.pk:
            # If new pk, set User.Type
            self.type = User.Types.SUPERVISOR
        return super().save(*args, **kwargs)


class CEOManager(models.Manager):
    """
    Model-Manager for Supervisors
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CEO)


class CEO(User):
    """
    Proxy User Model for CEOs (Geschäftsführer)
    """

    # Set Model Manager
    objects = CEOManager()

    # Define as Proxy Model (no database entry)
    class Meta:
        proxy = True

    # Override save, so type doesnt need an extra type-specification in the argument
    # Creating a new user is done by: CEO.create(name='',...)
    def save(self, *args, **kwargs):
        if not self.pk:
            # If new pk, set User.Type
            self.type = User.Types.CEO
        return super().save(*args, **kwargs)


class AdminManager(models.Manager):
    """
    Model-Manager for Supervisors
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)


class Admin(User):
    """
    Proxy User Model for Admins (Admins)
    """

    # Set Model Manager
    objects = AdminManager()

    # Define as Proxy Model (no database entry)
    class Meta:
        proxy = True

    # Override save, so type doesnt need an extra type-specification in the argument
    # Creating a new user is done by: Admin.create(name='',...)
    def save(self, *args, **kwargs):
        if not self.pk:
            # If new pk, set User.Type
            self.type = User.Types.ADMIN
        return super().save(*args, **kwargs)
