# users/models.py
import logging
import datetime
from dataclasses import dataclass
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from core.models import (CoreDataModel, FieldMetadata,
                         CompanySite, ReturnValuesMixin)
from core.constants import UserRoles
from core.models import FieldMetadata
from users.constants import UserCoreFields
from users.constants import UserCoreFields
from customers.constants import CustomerCoreFields
from customers.models import CustomerFieldListVisibility


def build_username(lastname: str, firstname: str):
    """
    Build a username from firstname and lastname
    """
    # Normalize lastname and firstname
    lastname_norm = lastname.replace(" ", "").lower().replace(
        'ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss')
    firstname_norm = firstname.replace(" ", "").lower().replace(
        'ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss')
    # Create username
    username = firstname_norm+lastname_norm

    # If users with same combination of firstname and lastname exist
    # , add a number to the end (username has to be unique)
    existing_users = User.objects.filter(
        username__contains=username).count()

    if existing_users > 0:
        # Now check if the username is available (if users were deleted
        # inbetween, it might assign taken numbers)
        available_username_found = False

        while not available_username_found:
            # Create the new username
            username = username + '_' + str(existing_users)

            if User.objects.filter(username__contains=username).count() == 0:
                # Valid username was found
                available_username_found = True
            else:
                # Increase number
                existing_users += 1

                # To avoid infinite loop
                if existing_users == 999:
                    raise ValueError(
                        'Too many users with firstname and lastname')

    return username


def create_customerfieldlistvisibility_new_user(user):
    """
    create customer field visibility settings for the new user
    """

    # Core Fields
    for field in CustomerCoreFields.get_fields():

        # Get fieldinfo of core fields
        fieldinfo = CustomerCoreFields.get_fieldinfo_by_name(field['name'])

        setting = CustomerFieldListVisibility.objects.create(
            fieldname=field['name'], visible=fieldinfo['visible'], user=user)
        setting.save()

    # Custom Fields (per default invisible)
    for field in FieldMetadata.objects.filter(kind='customer'):
        setting = CustomerFieldListVisibility.objects.create(
            fieldname=field.name, visible=field.default_visible, user=user)
        setting.save()


def create_userfieldlistvisibility_new_user(user):
    """
    create user field visibility settings for the new user
    """

    # Core Fields
    for field in UserCoreFields.get_fields():

        # Get fieldinfo of core fields
        fieldinfo = UserCoreFields.get_fieldinfo_by_name(field['name'])

        setting = UserFieldListVisibility.objects.create(
            fieldname=field['name'], visible=fieldinfo['visible'], user=user)
        setting.save()

    # Custom Fields (per default invisible)
    for field in FieldMetadata.objects.filter(kind='user'):
        setting = UserFieldListVisibility.objects.create(
            fieldname=field.name, visible=field.default_visible, user=user)
        setting.save()


class UserManager(BaseUserManager):
    """
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    """

    def create_user(self, username: str,
                    role: str = UserRoles.CAREGIVER,
                    password: str = None,  **kwargs):
        """
        Create and return a User
        """
        # Required Fields
        if not password:
            raise ValueError('Please provide a password')

        if User.objects.filter(username=username, deleted=False).exists():
            raise ValueError('Username already existing')

        # Create user instance
        user = self.model(
            username=username,
            role=role,
            **kwargs
        )

        # Hash password
        user.set_password(password)

        # If Admin, set superuser and staff to true
        if role == 'ADMIN':
            user.is_superuser = True
            user.is_staff = True

        # Save user instance
        user.save(using=self._db)

        # Create field visibility settings for user
        create_userfieldlistvisibility_new_user(user)
        create_customerfieldlistvisibility_new_user(user)

        return user

    def create_superuser(self, username: str, password: str, **kwargs):

        # if 'role' was set via api-call
        kwargs.pop('role', None)

        if User.objects.filter(username=username, deleted=False).exists():
            raise ValueError('Username already existing')

        user = self.model(
            username=username,
            role=UserRoles.ADMIN,
            **kwargs
        )
        # Hash password
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        # Create field visibility settings for user
        create_userfieldlistvisibility_new_user(user)
        create_customerfieldlistvisibility_new_user(user)

        return user


class User(CoreDataModel, AbstractUser):
    """
    General User Model
    """

    first_name = None
    last_name = None

    class Roles(models.TextChoices):
        CAREGIVER = UserRoles.CAREGIVER, 'Alltagshelfer'
        SUPERVISOR = UserRoles.SUPERVISOR, 'Teamleiter'
        CEO = UserRoles.CEO, 'Geschäftsführer'
        ADMIN = UserRoles.ADMIN, 'Administrator'

    # User Fields
    author = models.ForeignKey("users.User", on_delete=models.DO_NOTHING,
                               blank=True, null=True,
                               verbose_name=_('Ersteller'))
    role = models.CharField(max_length=50, choices=Roles.choices,
                            default=Roles.CAREGIVER,
                            verbose_name=_('Benutzer-Typ'))
    companysite = models.ForeignKey(
        CompanySite, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(
        max_length=200, blank=True, null=True, unique=True,
        verbose_name=_('Benutzername'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    invalidate_before = models.DateTimeField(
        blank=True, null=True, verbose_name=_(
            'Zeitpunkt der letzten Token-entwertung'))
    custom_fields = models.ManyToManyField(
        FieldMetadata,
        through='UserFieldValue',
        through_fields=('user', 'field'),
        verbose_name=_('Benutzerdefinierte Felder für Mitarbeiter'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this role.
    objects: UserManager = UserManager()

    def __str__(self):
        return self.username

    def delete(self):
        self.deleted = True
        self.deleted_at = make_aware(datetime.datetime.now())
        self.save()
        return True

    class Meta:
        verbose_name_plural = _('Benutzer')
        verbose_name = _('Benutzer')
        db_table = "users"
        ordering = ["-date_joined"]


class UserFieldValue(models.Model):
    """
    Model for Custom User Field Values
    """

    field = models.ForeignKey(
        FieldMetadata, on_delete=models.CASCADE, verbose_name=_('Feld'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Mitarbeiter'))
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
        db_table = "user_fields_values"
        verbose_name_plural = _('Benutzerdefinierte Felder')
        verbose_name = _('Benutzerdefiniertes Feld')


class UserFieldListVisibility(ReturnValuesMixin, models.Model):
    """
    Model for visibility settings (in list) of fields per user
    """
    fieldname = models.CharField(max_length=255, verbose_name=_('Feld'))
    visible = models.BooleanField(default=False, verbose_name=_('Sichtbar'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Benutzer'))

    def __str__(self):
        return str(self.fieldname)

    class Meta:
        db_table = "user_fields_visbility"
        verbose_name_plural = _('Sichtbarkeit der Benutzerfelder in Übersicht')
        verbose_name = _('Sichtbarkeit der Benutzerfelder in Übersicht')
