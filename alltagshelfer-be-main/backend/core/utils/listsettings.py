# core/utils/listsettings.py

from core.constants import Kind
from users.models import (User, UserFieldListVisibility)
from customers.models import CustomerFieldListVisibility


def create_fieldlistvisibility_new_field(name: str, default_visible: str, kind: str):
    if kind == Kind.USER:
        return create_userfieldlistvisibility_entry(name, default_visible)
    elif kind == Kind.CUSTOMER:
        return create_customerfieldlistvisibility_entry(name, default_visible)
    else:
        return False


def create_userfieldlistvisibility_entry(name: str, default_visible: str):

    if UserFieldListVisibility.objects.filter(fieldname=name).count() == 0:
        # add field to field visibility list
        for user in User.objects.all():
            UserFieldListVisibility.objects.create(
                fieldname=name, visible=default_visible, user=user)
        return True
    else:
        # Field exists already
        return False


def create_customerfieldlistvisibility_entry(name: str, default_visible: str):

    if CustomerFieldListVisibility.objects.filter(fieldname=name).count() == 0:
        # add field to field visibility list
        for user in User.objects.all():
            CustomerFieldListVisibility.objects.create(
                fieldname=name, visible=default_visible, user=user)
        return True
    else:
        # Field exists already
        return False
