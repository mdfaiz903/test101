# core/validators/reorder_validator.py

import logging
from api.utilities import GenericAPIException
from rest_framework import status
from core.constants import Kind
from core.models import FieldMetadata


def validate(kind, order):

    # check if kind and order were given
    if kind is None:
        # raise exception
        raise GenericAPIException(
            detail={'kind': 'Dieses Feld darf nicht null sein.'},
            status_code=status.HTTP_400_BAD_REQUEST)
    if order is None:
        # raise exception
        raise GenericAPIException(
            detail={'order': 'Dieses Feld darf nicht null sein.'},
            status_code=status.HTTP_400_BAD_REQUEST)

    # check if kind is user or customer
    if kind == Kind.USER or kind == Kind.CUSTOMER:
        pass
    else:
        # raise exception
        raise GenericAPIException(
            detail={'kind': 'Auswahl nicht vorhanden'},
            status_code=status.HTTP_400_BAD_REQUEST)

    # check if length of positions is the same as the number of fieldmetadata
    if len(order) != FieldMetadata.objects.filter(kind=kind).count():
        # raise exception
        raise GenericAPIException(
            detail={'position': 'Unvollständig oder fehlerhaft.'},
            status_code=status.HTTP_400_BAD_REQUEST)

    # check if positions are valid (start at 0, increments one by one)
    current_pos = 0
    for item in order:
        if item['position'] < current_pos or item['position'] > current_pos:
            # raise exception
            raise GenericAPIException(
                detail={'position': 'Unvollständig oder fehlerhaft'},
                status_code=status.HTTP_400_BAD_REQUEST)
        current_pos += 1

    return True
