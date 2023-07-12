# core/utils/reorder.py

import logging
from core.constants import Kind
from core.models import FieldMetadata
from django.shortcuts import get_object_or_404


def reorder(kind, order):
    """
    reorder fieldmetadata
    """

    for item in order:
        field_to_reorder = get_object_or_404(
            FieldMetadata, id=item['id'])
        field_to_reorder.position = item['position']
        field_to_reorder.save()
    return True
