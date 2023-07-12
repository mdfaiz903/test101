# core/validators/field_validators.py

import logging
import datetime
from core.constants import DataTypes, InputTypes
from users.models import UserFieldValue
from customers.models import CustomerFieldValue


def perform_value_datatype_validation(val, data_type):
    """
    perform value-datatype validation
    first, determine if it a single value or a list
    """
    # BOOLEAN
    if data_type == DataTypes.BOOLEAN:
        if val.lower() == 'true' or val.lower() == 'false' or \
                val is True or val is False:
            pass
        else:
            return False

    # INTEGER
    elif data_type == DataTypes.INT:
        if val.isdigit():
            pass
        else:
            return False

    # FLOAT
    elif data_type == DataTypes.FLOAT:
        try:
            float(val.replace(',', '.'))
        except (ValueError, AttributeError):
            return False

    # DATE
    elif data_type == DataTypes.DATE:
        try:
            datetime.date.fromisoformat(val)
        except ValueError:
            return False
        # Pass if val is None (nothing stored)
        except TypeError:
            if val is None:
                pass

    # STRING
    elif data_type == DataTypes.STRING:
        # It is always string
        pass

    return True


def validate_datatype(value, data_type):
    """
    validate datatype
    first, determine if it a single value or a list
    """

    # If it is a list of values,
    if type(value) == list:
        validation = True
        for val in value:
            if not perform_value_datatype_validation(val, data_type):
                validation = False
        return validation
    else:
        return perform_value_datatype_validation(value, data_type)


def perform_value_selection_validation(val, enums, input_type):

    if input_type == InputTypes.SELECT:
        # Check if val is at least one of the specified values
        if any(enum == str(val)
                for enum in enums):
            pass
        else:
            return False

    elif input_type == InputTypes.MULTISELECT:
        # Check if val is at least one of the specified values
        if any(enum == str(val)
                for enum in enums):
            pass
        else:
            return False

    # Invalid InputType
    else:
        return False

    return True


def validate_selection(value, enums, input_type):
    """
    validate selection
    can be used for select and multiselect
    val can be a list or a single value (depends on the input type)
    """

    # If it is a list of values,
    if isinstance(value, list):
        # Return False if any of the values is not a valid selection
        for val in value:
            if perform_value_selection_validation(val, enums, input_type):
                pass
            else:
                return False
        return True
    else:
        return perform_value_selection_validation(value, enums, input_type)

    return True


def validate_parameters_for_input_type(data, input_type):
    """
    check if handed data fits to coresponding input type
    """

    # Multiselect
    if input_type == InputTypes.MULTISELECT:
        if data.get('placeholder', None):
            return False
        elif data.get('enums', None) is None:
            return False

    # Select
    elif input_type == InputTypes.SELECT:
        if data.get('placeholder', None):
            return False
        elif data.get('enums', None) is None:
            return False

    # Checkbox
    elif input_type == InputTypes.CHECKBOX:
        if data.get('placeholder', None):
            return False
        elif data.get('enums', None):
            return False

    # Input
    elif input_type == InputTypes.INPUT:
        if data.get('enums', None):
            return False

    # Date
    elif input_type == InputTypes.DATE:
        if data.get('placeholder', None):
            return False
        elif data.get('enums', None):
            return False

    # Invalid InputType
    else:
        return False

    return True


def check_if_enum_is_unused(val, field):
    # Check if user or customer has used enum value
    for customerfield in CustomerFieldValue.objects.filter(field=field):
        if val in customerfield.value:
            return False
    for userfield in UserFieldValue.objects.filter(field=field):
        if val in userfield.value:
            return False

    return True
