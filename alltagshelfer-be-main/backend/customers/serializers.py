# customers/serializers.py

import pytz
import logging
import datetime
from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from alltagshelfer_be.settings import TIME_ZONE
from .models import (Customer, CustomerFieldValue,
                     CustomerFieldListVisibility)
from .constants import CustomerCoreFields
from core.models import FieldMetadata, FieldType
from core.constants import DataTypes, InputTypes, Kind
from core.utils import serializer_utils
from core.validators import field_validators


class CustomerListCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for User model (ListCreateAPIView)
    """

    # Custom field values
    field_values = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('__all__')
        fields_not_returned = ['custom_fields', 'deleted', 'deleted_at', 'id']
        required_input_fields = ['salutation', 'firstname', 'lastname',
                                 'street', 'house_number',
                                 'city', 'zip', 'birthday']

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        values = serializer_utils.get_field_values(Kind.CUSTOMER, obj, False,
                                                   self.Meta.fields_not_returned,
                                                   user=self.context['user'])

        return sorted(values, key=lambda k: k['position'])

    def validate(self, data):
        """
        check if required fields were given
        """

        for field in self.Meta.required_input_fields:
            if field not in data:
                raise serializers.ValidationError(
                    {str(field): 'Dieses Feld ist erforderlich'})
        return data

    def create(self, validated_data):
        """
        create new instance of user, with given validated data
        """

        return Customer.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        edit the representation of the output
        """

        representation_full = super().to_representation(instance)

        representation = {'id': representation_full['id'],
                          'field_values': representation_full['field_values']}

        # Get representational response
        return representation


class CustomerListCreateFullSerializer(CustomerListCreateSerializer):

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        values = serializer_utils.get_field_values(Kind.CUSTOMER, obj, True,
                                                   self.Meta.fields_not_returned,
                                                   user=self.context['user'])

        return sorted(values, key=lambda k: k['position'])


class CustomerRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer for User model (RetrieveUpdateDestroyAPIView)
    """

    # Custom field values
    field_values = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        exclude = ('deleted', 'deleted_at')
        fields_not_returned = ['custom_fields', 'deleted', 'deleted_at', 'id']
        # These values are not listed as "field_values"
        exluded_field_values = ['id']

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        values = serializer_utils.get_field_values(Kind.CUSTOMER, obj, True,
                                                   self.Meta.fields_not_returned,
                                                   user=self.context['user'])

        return sorted(values, key=lambda k: k['position'])

    def to_representation(self, instance):
        """
        here the representation of the output can be edited
        """

        representation_full = super().to_representation(instance)

        representation = {'id': instance.id,
                          'field_values': representation_full['field_values']}

        # Get representational response
        return representation


class CustomerFieldValueSerializer(serializers.ModelSerializer):
    """
    Serializer for customer fields
    """

    class Meta:
        model = CustomerFieldValue
        exclude = ('customer',)

    def to_representation(self, instance):
        """
        edit the representation of the output
        """

        # Get response
        representation_full = super().to_representation(instance)

        field = instance.field

        try:
            # If more than one value, preserve list
            if len(representation_full['value']) > 1:
                pass
            # If only one value, get first one
            elif len(representation_full['value']) == 1:
                representation_full['value'] = representation_full['value'][0]
        except TypeError:
            # Value is None
            representation_full['value'] = None

        # Build dict for representation
        representation = {
            'id': field.id,
            'title': FieldMetadata.objects.get(
                id=representation_full['field']).title,
            'value': representation_full['value']
        }

        # Get representational response
        return representation

    def validate(self, data):
        """
        if field is created/updated, check if
        1) transmitted value fits its corresponding data type
        2) the value is one of the selection-values (if specified as select)
        """

        # 1)
        # Get specified data_type field
        field_type_id = data['field'].field_type_id

        data_type = FieldType.objects.get(
            id=int(field_type_id)).data_type

        # Message for data_type mismatch
        msg = 'data_type mismatch'

        # Check if data_type has expected format
        if field_validators.validate_datatype(data['value'], data_type):
            pass
        else:
            raise serializers.ValidationError(
                msg)

        # 3)
        # Message for input_type mismatch
        msg = 'select value mismatch'

        input_type = FieldType.objects.get(
            id=int(field_type_id)).input_type

        if input_type == InputTypes.SELECT or input_type == InputTypes.MULTISELECT:
            # Check if data_type has expected format
            if field_validators.validate_selection(data['value'],
                                                   data['field'].enums,
                                                   input_type):
                pass
            else:
                raise serializers.ValidationError(
                    msg)

        return data

    def create(self, validated_data):
        """
        create new field
        """

        # Get user
        # Check if CustomerField was already added before
        customer = get_object_or_404(Customer, id=self.context['id'])
        try:
            # Get field
            field = CustomerFieldValue.objects.get(
                field=validated_data['field'], customer=customer)
            # Update value
            field.value = validated_data['value']
            # Save field
            field.save()

        except CustomerFieldValue.DoesNotExist:
            field = CustomerFieldValue.objects.create(
                field=validated_data['field'], customer=customer,
                value=validated_data['value'])

        return field

################################################################


class CustomerFieldListVisibilitySerializer(serializers.ModelSerializer):
    """
    Serializer for customer field list visibility
    """

    class Meta:
        model = CustomerFieldListVisibility
        fields = ('fieldname', 'visible', 'user')

    def validate(self, data):
        """
        validate
        """

        try:
            # check if field exists in FieldMetadata
            FieldMetadata.objects.get(name=data['fieldname'])
        except FieldMetadata.DoesNotExist:
            # check if field exists in Core Fields
            if CustomerCoreFields.get_fieldinfo_by_name(data['fieldname'])['exists']:
                pass
            else:
                raise serializers.ValidationError(
                    {data['fieldname']: 'Feld existiert nicht'})

        return data

    def create(self, validated_data):
        """
        change setting
        """

        # check if setting existst
        try:
            customer_field_list_visibility = CustomerFieldListVisibility.objects.get(
                fieldname=validated_data['fieldname'],
                user=validated_data['user'])

            customer_field_list_visibility.visible = validated_data['visible']

            customer_field_list_visibility.save()

        except CustomerFieldListVisibility.DoesNotExist:
            customer_field_list_visibility = CustomerFieldListVisibility.objects.create(
                fieldname=validated_data['fieldname'],
                user=validated_data['user'],
                visible=validated_data['visible'])

        return customer_field_list_visibility
