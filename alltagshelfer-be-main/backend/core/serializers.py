# core/serializers.py
import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from core.models import FieldMetadata, FieldType, CompanySite
from users.models import UserFieldListVisibility
from core.validators import field_validators
from core.utils import listsettings
from core.constants import DataTypes, InputTypes


def validate_field_parameters(data, field_type):
    # If boolean-checkbox
    if field_type == FieldType.objects.get(id=1):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Checkboxen werden Placeholder nicht akzeptiert")
        # 2) no enums
        if data['enums'] is not None:
            raise serializers.ValidationError(
                "Für Checkboxen werden Enums nicht akzeptiert")
    # If Integer-Input
    elif field_type == FieldType.objects.get(id=2):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Integer Inputs werden Placeholder nicht akzeptiert")
        # 2) no enums
        if data['enums'] is not None:
            raise serializers.ValidationError(
                "Für Integer Inputs werden Enums nicht akzeptiert")
    # If Integer-Dropdown
    elif field_type == FieldType.objects.get(id=3):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Integer Inputs werden Placeholder nicht akzeptiert")
        # 2) enums
        if data['enums'] is None:
            raise serializers.ValidationError(
                "Für Integer Dropdowns sind enums (mit ; getrennt) erforderlich")
        # 3) enums shall be integers
        for val_int in data['enums']:
            try:
                int(val_int)
            except ValueError:
                raise serializers.ValidationError(
                    "Alle Werte des Enums müssen für Integer sein")
    # If Float-Input
    elif field_type == FieldType.objects.get(id=4):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Float Inputs werden Placeholder nicht akzeptiert")
        # 2) no enums
        if data['enums'] is not None:
            raise serializers.ValidationError(
                "Für Float Inputs werden Enums nicht akzeptiert")
    # If Float-Dropdown
    elif field_type == FieldType.objects.get(id=5):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Float Dropdowns werden Placeholder nicht akzeptiert")
        # 2) enums
        if data['enums'] is None:
            raise serializers.ValidationError(
                "Für Float Dropdowns sind enums erforderlich")
        # 3) enums shall be integers
        for val_int in data['enums']:
            try:
                float(val_int.replace(',', '.'))
            except (ValueError, AttributeError):
                raise serializers.ValidationError(
                    "Alle Werte des Enums müssen für Gleitkommazahlen sein")
    # If String-Input
    elif field_type == FieldType.objects.get(id=6):
        # 1) no enums
        if data['enums'] is not None:
            raise serializers.ValidationError(
                "Für String Inputs werden Enums nicht akzeptiert")
    # If String-Dropdown
    elif field_type == FieldType.objects.get(id=7):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für String Dropdowns werden Placeholder nicht akzeptiert")
        # 2) enums
        if data['enums'] is None:
            raise serializers.ValidationError(
                "Für String Dropdowns sind enums (mit ; getrennt) erforderlich")
    # If Date-Date
    elif field_type == FieldType.objects.get(id=8):
        # 1) no placeholder
        if data['placeholder'] is not None:
            raise serializers.ValidationError(
                "Für Datum-Felder werden Placeholder nicht akzeptiert")
        # 2) no enums
        if data['enums'] is not None:
            raise serializers.ValidationError(
                "Für Datum-Felder werden Enums nicht akzeptiert")
    # Unsupported Field_Type
    else:
        pass


class FieldMetadataListSerializer(serializers.ModelSerializer):
    """
    serializer Class for FieldMetaData List
    """

    field_type = serializers.SerializerMethodField()

    class Meta:
        model = FieldMetadata
        fields = ['id', 'name', 'kind', 'default_visible', 'field_type', 'position',
                  'placeholder', 'enums', 'title', 'required']
        read_only_fields = ('position',)
        # unique together validators
        validators = [
            UniqueTogetherValidator(
                queryset=FieldMetadata.objects.all(),
                fields=['title', 'kind'])  # ,
            # UniqueTogetherValidator(
            #    queryset=FieldMetadata.objects.all(),
            #    fields=['position', 'kind'])
        ]

    def get_field_type(self, obj):
        """
        display linked field_type of FieldMeta
        """

        # Get field_type_id
        field_type_id = int(obj.field_type_id)

        data_type = FieldType.objects.get(id=field_type_id).data_type
        input_type = FieldType.objects.get(id=field_type_id).input_type

        field_type = {
            'id': field_type_id,
            'input_type': input_type,
            'data_type': data_type
        }

        return field_type

    def validate(self, data):
        """
        on create, check if
        1) if a valid field_type_id was specified
        2) If the given field parameters are valid
        3) Enum values are valid
        4) if "default_visible" was specified
        """

        # 1) Valid Field-Type?

        # Check if there is an field_type_id in transmitted data
        try:

            field_type = self.initial_data['field_type']

            field_type_id = field_type['id']

            field_type = FieldType.objects.get(id=field_type_id)

        except KeyError:
            raise serializers.ValidationError(
                "Field Type ID fehlt")
        except FieldType.DoesNotExist:
            raise serializers.ValidationError(
                "Field Type existiert nicht")

        # 2) Valid field parameters for specified input type?
        if field_validators.validate_parameters_for_input_type(
                data, field_type.input_type):
            pass
        else:
            raise serializers.ValidationError(
                "Data und Field Type Mismatch")

        # 3) If select or multiselect, check if enum values are valid
        if field_type.input_type == InputTypes.SELECT or field_type.input_type == InputTypes.MULTISELECT:
            for enum in data['enums']:
                if field_validators.validate_datatype(
                        enum, field_type.data_type):
                    pass
                else:
                    raise serializers.ValidationError(
                        "Data und Data Type Mismatch")

        # 4)
        try:

            default_visible = self.initial_data['default_visible']

        except KeyError:
            raise serializers.ValidationError(
                "Default_visible missing")

        # If everything is valid, add field type id to data
        data['field_type_id'] = field_type_id

        return data

    def create(self, validated_data):
        """
        Create new instance of FieldMetadata
        """

        try:
            # Get highest position
            pos = FieldMetadata.objects.filter(
                kind=validated_data['kind']).order_by('-position')[0].position
        except IndexError:
            # No field available
            pos = -1

        # Set position
        validated_data['position'] = pos + 1

        # Create FieldMetadata
        instance = FieldMetadata.objects.create(**validated_data)

        # check if user or customer field
        if listsettings.create_fieldlistvisibility_new_field(
                instance.name, validated_data['default_visible'], validated_data['kind']):
            pass
        else:
            raise serializers.ValidationError(
                "Fehler")
        return instance


class FieldMetaDataRetrieveUpdateDestroySerializer(
        serializers.ModelSerializer):
    """
    serializer Class for existing single FieldMetadata
    """

    class Meta:
        model = FieldMetadata
        fields = ['id', 'name', 'kind', 'default_visible', 'field_type', 'position',
                  'placeholder', 'enums', 'title', 'required']
        read_only_fields = ('position', 'field_type')
        # unique together validators
        validators = [
            UniqueTogetherValidator(
                queryset=FieldMetadata.objects.all(),
                fields=['title', 'kind'])
        ]

    field_type = serializers.SerializerMethodField()

    def get_field_type(self, obj):
        """
        display linked field_type of FieldMeta
        """

        # Get field_type_id
        field_type_id = int(obj.field_type_id)

        data_type = FieldType.objects.get(id=field_type_id).data_type
        input_type = FieldType.objects.get(id=field_type_id).input_type
        field_type = {
            'id': field_type_id,
            'input_type': input_type,
            'data_type': data_type
        }

        return field_type

    def validate(self, data):
        """
        on update, check if
        1) the field parameters are valid for the existing field_type
        2) if default_visible was included
        3) no used enums are deleted
        """

        # 1)
        field = FieldMetadata.objects.get(
            id=self.context['fieldpk'])

        # Valid field parameters for specified input type?
        if field_validators.validate_parameters_for_input_type(
                data, field.field_type.input_type):
            pass
        if data.get('enums',
                    None) and field_validators.validate_datatype(
                data['enums'], field.field_type.data_type):
            pass
        else:
            raise serializers.ValidationError(
                "Data und Field Type Mismatch")

        # 2)
        try:
            default_visible = self.initial_data['default_visible']
        except KeyError:
            raise serializers.ValidationError(
                "Default_visible missing")

        # 3)
        if field.field_type.input_type == InputTypes.SELECT or field.field_type.input_type == InputTypes.MULTISELECT:
            new_enum_list = data['enums']
            old_enum_list = field.enums
            enum_values_to_be_deleted = old_enum_list
            for enum_val in new_enum_list:
                if enum_val in old_enum_list:
                    enum_values_to_be_deleted.remove(enum_val)
            for val in enum_values_to_be_deleted:
                if not field_validators.check_if_enum_is_unused(val, field):
                    # Return a set of the actual enums and the transmitted enums
                    # so that if the user tries to add an enum and delete a used one,
                    # the deleted ones are shown in the form again
                    raise serializers.ValidationError(
                        {"error": "Enum is used",
                         "enums_complete": list(set(data['enums']+field.enums))})

        return data


class CompanySiteListSerializer(serializers.ModelSerializer):
    """
    serializer class for company sites
    """

    class Meta:
        model = CompanySite
        fields = ('__all__')


class CompanySiteDetailSerializer(serializers.ModelSerializer):
    """
    serializer class for company sites
    """

    class Meta:
        model = CompanySite
        fields = ('__all__')
