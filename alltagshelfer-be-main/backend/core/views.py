# core/views.py

import copy
import logging
from typing import Callable, Union
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from api.utilities import IsSupervisorMixin
from users.models import UserFieldListVisibility
from customers.models import CustomerFieldListVisibility
from users.constants import UserCoreFields
from customers.constants import CustomerCoreFields
from core.constants import Kind
from core.models import FieldMetadata, FieldType, CompanySite
from core.serializers import (FieldMetadataListSerializer,
                              FieldMetaDataRetrieveUpdateDestroySerializer,
                              CompanySiteListSerializer,
                              CompanySiteDetailSerializer)

from core.validators import reorder_validators
from core.utils import reorder


class FieldMetadataList(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-write endpoint for a list of fields meta data
    1) List all Fields Meta Data (GET)
    2) Create new Field (POST)
    """

    serializer_class = FieldMetadataListSerializer

    def get_queryset(self):
        """
        change queryset to return requested kind
        """

        queryset = FieldMetadata.objects.all()

        if self.kind is not None:
            queryset = queryset.filter(kind=self.kind)

        return queryset

    def get(self, request):
        """
        overwrite get method to add user core fields if requested
        """

        # Check if 'kind' was sent
        self.kind = self.request.query_params.get('kind', None)

        # Get serialized data
        serializer = FieldMetadataListSerializer(
            self.get_queryset(), many=True)
        serializer_data = list(serializer.data)

        # Check if full
        full_param = request.query_params.get('full')

        if not full_param:
            full_param = 'false'

        data: list = []

        if full_param == 'true':
            # Add core fields of user
            for field in copy.deepcopy(UserCoreFields.get_fields()):
                if self.kind == Kind.USER or self.kind is None:
                    # Get rid of unwanted fields
                    del field['input_type']
                    del field['data_type']
                    # get field visibility
                    field['visible'] = UserFieldListVisibility.objects.get(
                        fieldname=field['name'], user=request.user).visible
                    data.append(field)

            # Add core fields of user
            for field in copy.deepcopy(CustomerCoreFields.get_fields()):
                if self.kind == Kind.CUSTOMER or self.kind is None:
                    # Get rid of unwanted fields
                    del field['input_type']
                    del field['data_type']
                    # get field visibility
                    field['visible'] = CustomerFieldListVisibility.objects.get(
                        fieldname=field['name'], user=request.user).visible
                    data.append(field)

            if self.kind != Kind.CUSTOMER and self.kind != Kind.USER and self.kind != None:
                # Wrong kind
                return Response({'kind': 'Kind not existent.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Get length of data entries, to adjust position
        n_data = len(data)

        # Add fields
        for field in serializer_data:
            field['position'] += n_data
            data.append(field)

        return Response(sorted(data, key=lambda k: k['position']))

    def create(self, request, *args, **kwargs):

        # If enums is an empty list, save as None
        if request.data['enums'] == []:
            request.data['enums'] = None
        response = super().create(request, *args, **kwargs)

        return response


class FieldMetadataDetail(IsSupervisorMixin,
                          generics.RetrieveUpdateDestroyAPIView):
    """
    read-write-delete endpoint for a single FieldMetadata object
    1) View Field (GET)
    2) Update Field (PUT)
    3) Delete Field (DELETE)
    """

    serializer_class = FieldMetaDataRetrieveUpdateDestroySerializer

    def get_queryset(self):
        """
        change queryset to return requested kind
        """
        queryset = FieldMetadata.objects.all()
        kind = self.request.query_params.get('kind', None)
        if kind is not None:
            queryset = queryset.filter(kind=kind)

        return queryset

    def get_serializer_context(self):
        context = super(FieldMetadataDetail, self).get_serializer_context()
        # Pass field pk to serializer
        context['fieldpk'] = self.kwargs['fieldpk']

        return context

    def get(self, request, *args, **kwargs):
        # get requested fieldmetadata
        instance = get_object_or_404(FieldMetadata, id=kwargs['fieldpk'])
        # serialize data
        serializer = self.get_serializer(
            instance)
        # return data
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # If enums is an empty list, save as None
        if request.data['enums'] == []:
            request.data['enums'] = None

        # get requested fieldmetadata
        instance = get_object_or_404(FieldMetadata, id=kwargs['fieldpk'])
        # get fieldname before
        fieldname_before = instance.name

        # serialize data
        serializer = self.get_serializer(
            instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # perform update
        self.perform_update(serializer)
        # Get instance after change
        fieldname_after_update = FieldMetadata.objects.get(
            id=kwargs['fieldpk']).name

        # Exchange name
        if fieldname_before != fieldname_after_update:
            if instance.kind == Kind.USER:
                # Get visibility setting for old name (all users)
                field_visibility_settings = UserFieldListVisibility.objects.filter(
                    fieldname=fieldname_before)
            elif instance.kind == Kind.CUSTOMER:
                # Get visibility setting for old name (all users)
                field_visibility_settings = CustomerFieldListVisibility.objects.filter(
                    fieldname=fieldname_before)
            for field_visibility_setting in field_visibility_settings:
                # Set new fieldname
                field_visibility_setting.fieldname = fieldname_after_update
                # Save instance
                field_visibility_setting.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        # Get requested fieldmetadata
        instance = get_object_or_404(FieldMetadata, id=kwargs['fieldpk'])
        # get name
        name_of_deleted_field = instance.name
        # delete instance
        instance.delete()

        if instance.kind == Kind.USER:
            # delete visibility setting entries for deleted fieldmeta
            UserFieldListVisibility.objects.filter(
                fieldname=name_of_deleted_field).delete()
        elif instance.kind == Kind.CUSTOMER:
            # delete visibility setting entries for deleted fieldmeta
            CustomerFieldListVisibility.objects.filter(
                fieldname=name_of_deleted_field).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FieldMetadataReorder(IsSupervisorMixin, APIView):
    """
    write endpoint to reorder fieldmetadata
    1) Reorder fieldmetadata (POST)
    """

    queryset = FieldMetadata.objects.all()

    def put(self, request, *args, **kwargs):

        for data in request.data:
            kind = data.get('kind', None)
            order = data.get('order', None)

        # validate request
        reorder_validators.validate(kind, order)

        # perform reordering
        reorder.reorder(kind, order)

        fields = FieldMetadata.objects.filter(kind=kind)

        serializer = FieldMetadataListSerializer(
            fields, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldTypeList(IsSupervisorMixin, APIView):
    """
    read endpoint for a list of field types
    1) List all Field Types (GET)
    """

    def get(self, request, format=None):
        queryset = FieldType.objects.all().values()
        return Response(queryset)


class CompanySiteList(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-write endpoint for a list of company sites
    1) List all Company Sites (GET)
    2) Create new Company Site (POST)
    """

    queryset = CompanySite.objects.all()
    serializer_class = CompanySiteListSerializer


class CompanySiteDetail(IsSupervisorMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    """
    read-write-delete endpoint for a single company site object
    1) View Company Site (GET)
    2) Update Company Site (PUT)
    3) Delete Company Site (DELETE)
    """

    queryset = CompanySite.objects.all()
    serializer_class = CompanySiteDetailSerializer

    def get(self, request, *args, **kwargs):
        # get requested companysite
        instance = get_object_or_404(CompanySite, id=kwargs['pk'])
        # instance = CompanySite.objects.get(id=kwargs['pk'])
        # serialize data
        serializer = self.get_serializer(
            instance)
        # return data
        return Response(serializer.data)
