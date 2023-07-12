# core/utils/serializer_utils.py

import pytz
import logging
from rest_framework import status
from rest_framework.response import Response
from alltagshelfer_be.settings import TIME_ZONE
from users.constants import UserCoreFields
from customers.constants import CustomerCoreFields
from core.models import FieldMetadata, FieldType
from core.constants import DataTypes, InputTypes, Kind
from users.models import (User,
                          UserFieldValue,
                          UserFieldListVisibility)
from customers.models import (Customer,
                              CustomerFieldValue,
                              CustomerFieldListVisibility)


def get_field_values(kind,
                     obj,
                     should_include_all_fields: bool = False,
                     fields_not_returned: list[str] = [],
                     user=None) -> list[dict]:

    if kind == Kind.USER:
        current_model = User
        core_fields_model = UserCoreFields
        field_value_model = UserFieldValue
        list_visibility_model = UserFieldListVisibility
    elif kind == Kind.CUSTOMER:
        current_model = Customer
        core_fields_model = CustomerCoreFields
        field_value_model = CustomerFieldValue
        list_visibility_model = CustomerFieldListVisibility
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result = []
    skip_fields = fields_not_returned
    # Add base field values
    for field in current_model._meta.fields:
        if field.name in skip_fields:
            continue

        # Get core_field information for meta data
        fieldinfo = core_fields_model.get_fieldinfo_by_name(field.name)

        # Get value
        value = getattr(obj, field.name)

        # Get visible-info
        visible = list_visibility_model.objects.get(
            user=user, fieldname=field.name).visible
        # Set author to '', if admin
        if field.name == 'author':
            # Admin does not have an author
            try:
                value = value.username
            except AttributeError:
                value = None
        elif field.name == 'last_login':
            # Convert it to project-timezone
            if value is not None:
                value = value.astimezone(pytz.timezone(TIME_ZONE))

        if value is not None:
            value = str(value)

        result.append({
            'id': '0',
            'title': fieldinfo['title'],
            # Have to convert to string in case of foreignkey
            'value': value,
            'name': field.name,
            'position': fieldinfo['position'],
            'enums': fieldinfo['enums'],
            'placeholder': fieldinfo['placeholder'],
            'field_type': {
                'id': '0',
                'input_type': fieldinfo['input_type'],
                'data_type': fieldinfo['data_type']
            },
            'kind': kind,
            'visible': visible,
            'required': fieldinfo['required']
        })

    # Add custom field values
    if should_include_all_fields:
        all_fields = FieldMetadata.objects.filter(kind=kind)
        for field in all_fields:
            try:
                if kind == Kind.USER:
                    field_value = field_value_model.objects.get(
                        user=obj.id, field=field).value
                elif kind == Kind.CUSTOMER:
                    field_value = field_value_model.objects.get(
                        customer=obj.id, field=field).value
            except field_value_model.DoesNotExist:
                field_value = None

            # Get data type from field type object
            data_type = FieldType.objects.get(
                id=int(field.field_type_id)).input_type
            # Get input type from fieldtype object
            input_type = FieldType.objects.get(
                id=int(field.field_type_id)).data_type

            # Get visible-info
            visible = list_visibility_model.objects.get(
                user=user, fieldname=field.name).visible

            result.append({
                'id': field.id,
                'title': field.title,
                'value': field_value,
                'name': field.name,
                'position': len(result),
                'enums': field.enums,
                'placeholder': field.placeholder,
                'field_type': {
                    'id': int(field.field_type_id),
                    'input_type': input_type,
                    'data_type': data_type
                },
                'kind': field.kind,
                'visible': visible,
                'required': field.required
            })

    return result
