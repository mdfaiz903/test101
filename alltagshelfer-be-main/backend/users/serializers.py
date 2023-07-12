# users/serializers.py

import pytz
import logging
import datetime
from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from alltagshelfer_be.settings import TIME_ZONE
from .models import (User, UserFieldValue, build_username,
                     UserRoles, UserFieldListVisibility)
from .constants import UserCoreFields
from core.models import FieldMetadata, FieldType
from core.constants import DataTypes, InputTypes, Kind
from core.validators import field_validators
from core.utils import serializer_utils


class UserListCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for User model (ListCreateAPIView)
    """

    # Custom field values
    field_values = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('__all__')
        fields_not_returned = ['password', 'groups',
                               'user_permissions', 'custom_fields',
                               'created_at', 'is_active',
                               'is_staff', 'is_superuser', 'invalidate_before',
                               'deleted', 'deleted_at', 'id']
        required_input_fields = ['salutation', 'firstname', 'lastname',
                                 'password', 'street', 'house_number',
                                 'city', 'zip', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        values = serializer_utils.get_field_values(Kind.USER, obj, False,
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

        # Build username
        username = build_username(
            lastname=validated_data['lastname'],
            firstname=validated_data['firstname'])

        # Check if 'role' was given and if it is 'ADMIN'
        if validated_data.get('role') == UserRoles.ADMIN:
            return User.objects.create_superuser(
                username=username,
                author=self.context['request'].user,
                **validated_data)

        return User.objects.create_user(username=username,
                                        author=self.context['request'].user,
                                        **validated_data)

    def to_representation(self, instance):
        """
        edit the representation of the output
        """

        representation_full = super().to_representation(instance)

        representation = {'id': representation_full['id'],
                          'username': representation_full['username'],
                          'field_values': representation_full['field_values']}

        # Get representational response
        return representation


class UserListCreateFullSerializer(UserListCreateSerializer):

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        values = serializer_utils.get_field_values(Kind.USER, obj, True,
                                                   self.Meta.fields_not_returned,
                                                   user=self.context['user'])

        return sorted(values, key=lambda k: k['position'])


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer for User model (RetrieveUpdateDestroyAPIView)
    """

    # Custom field values
    field_values = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'lastname', 'firstname')
        fields_not_returned = ['password', 'groups',
                               'user_permissions', 'custom_fields',
                               'created_at', 'is_active',
                               'is_staff', 'is_superuser', 'invalidate_before',
                               'deleted', 'deleted_at', 'id']
        extra_kwargs = {'password': {'write_only': True}}
        # These values are not listed as "field_values"
        exluded_field_values = ['id']

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """
        values = serializer_utils.get_field_values(Kind.USER, obj, True,
                                                   self.Meta.fields_not_returned,
                                                   user=obj)

        return sorted(values, key=lambda k: k['position'])

    def to_representation(self, instance):
        """
        here the representation of the output can be edited
        """

        representation_full = super().to_representation(instance)

        representation = {'id': representation_full['id'],
                          'username': representation_full['username'],
                          'field_values': representation_full['field_values']}

        # Get representational response
        return representation


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, data):
        """
        Check if
        1) both passwords are the same
        2) password meet strength requirements
        """

        # 1) both passwords are the same
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                "Passwörter stimmen nicht überein")

        # 2) validated by django default password validation
        try:
            validate_password(data['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def update(self, instance, validated_data):
        """
        Update password
        """

        # Change password of user
        instance.set_password(validated_data['password'])

        # Save instance
        instance.save()

        return instance


class UserFieldValueSerializer(serializers.ModelSerializer):
    """
    Serializer for user fields
    """

    class Meta:
        model = UserFieldValue
        exclude = ('user',)

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

        # 2)

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
        create/update field value
        """

        # Get user
        # Check if UserField was already added before
        user = get_object_or_404(User, id=self.context['id'])
        try:
            # Get field
            field = UserFieldValue.objects.get(
                field=validated_data['field'], user=user)
            # Update value
            field.value = validated_data['value']
            # Save field
            field.save()

        except UserFieldValue.DoesNotExist:
            field = UserFieldValue.objects.create(
                field=validated_data['field'], user=user,
                value=validated_data['value'])

        return field


class UserFieldValueRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer for single user field
    """

    class Meta:
        model = UserFieldValue
        exclude = ('user', 'field')

    def validate(self, data):
        """
        Check if
        1) transmitted value fits its corresponding data type
        2) the value is one of the select-values (if specified as select)
        """

        # Get data from context
        field = FieldMetadata.objects.get(id=self.context['field'])

        # Add field to data
        data['field'] = field

        # 1)
        # Get specified data_type field
        field_type_id = field.field_type_id

        data_type = FieldType.objects.get(
            id=int(field_type_id)).data_type

        # Message for data_type mismatch
        datatype_mismatch_msg = 'data_type mismatch'

        # Check if data_type has expected format
        if field_validators.validate_datatype(data['value'], data_type):
            pass
        else:
            raise serializers.ValidationError(
                datatype_mismatch_msg)

        # 2)

        # Message for input_type mismatch
        value_mismatch_msg = '(multi)select value mismatch'

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
                    value_mismatch_msg)

        return data

    def update(self, instance, validated_data):
        """
        update field
        """

        # Get user
        # Check if UserField was already added before
        user = get_object_or_404(User, id=self.context['id'])
        # Get field
        field = UserFieldValue.objects.get(
            field=validated_data['field'], user=user)
        # Update value
        field.value = validated_data['value']
        # Save field
        field.save()

        return field

    def to_representation(self, instance):
        """
        edit the representation of the output
        """

        representation_full = super().to_representation(instance)

        field = FieldMetadata.objects.get(id=self.context['field'])

        #  Modify representation
        representation = {'id': field.id,
                          'value': representation_full['value'],
                          'title': field.title}

        # Get representational response
        return representation


class UserFieldListVisibilitySerializer(serializers.ModelSerializer):
    """
    Serializer for user field list visibility
    """

    class Meta:
        model = UserFieldListVisibility
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
            if UserCoreFields.get_fieldinfo_by_name(data['fieldname'])['exists']:
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
            user_field_list_visibility = UserFieldListVisibility.objects.get(
                fieldname=validated_data['fieldname'],
                user=validated_data['user'])

            user_field_list_visibility.visible = validated_data['visible']

            user_field_list_visibility.save()

        except UserFieldListVisibility.DoesNotExist:
            user_field_list_visibility = UserFieldListVisibility.objects.create(
                fieldname=validated_data['fieldname'],
                user=validated_data['user'],
                visible=validated_data['visible'])

        return user_field_list_visibility
