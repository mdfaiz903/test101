# customers/views.py

import logging
from typing import Callable, Union
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from api.utilities import (IsUserOrSupervisorMixin, IsSupervisorMixin,
                           IsAuthenticatedMixin)
from users.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer, CustomerFieldValue, CustomerFieldListVisibility
from customers.serializers import (
    CustomerListCreateSerializer,
    CustomerListCreateFullSerializer,
    CustomerRetrieveUpdateDestroySerializer,
    CustomerFieldValueSerializer,
    CustomerFieldListVisibilitySerializer)


class CustomerList(IsAuthenticatedMixin, generics.ListCreateAPIView):
    """
    read-write endport for a list of customers
    1) List all Users (GET)
    2) Create new User (POST)
    """

    queryset = Customer.objects.filter(deleted=False)
    serializer_classes: dict[str, Callable] = {
        'true': CustomerListCreateFullSerializer,
        'false': CustomerListCreateSerializer
    }

    def get_serializer_class(self) -> Union[
            CustomerListCreateSerializer,
            CustomerListCreateFullSerializer]:
        full_param = self.request.query_params.get('full')

        if not full_param:
            full_param = 'false'
        return self.serializer_classes[full_param]

    def get_serializer_context(self):
        context = super(CustomerList, self).get_serializer_context()
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context


class CustomerDetail(IsAuthenticatedMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    read-write-delete endpoint for a single customer
    1) View Customer (GET)
    2) Update Customer (PUT)
    3) Delete Customer (DELETE)
    """

    queryset = Customer.objects.filter(deleted=False)
    serializer_class = CustomerRetrieveUpdateDestroySerializer

    def get_serializer_context(self):
        context = super(CustomerDetail, self).get_serializer_context()
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context


class CustomerFieldList(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-write endpoint for a list of fields for a specific customer
    1) Get all Fields (GET)
    2) Create new Field for specified Customer (POST)
    """

    queryset = CustomerFieldValue.objects.all()
    serializer_class = CustomerFieldValueSerializer

    def get_queryset(self):
        # Get user

        customer = get_object_or_404(Customer, id=self.kwargs['pk'])

        return CustomerFieldValue.objects.filter(customer=customer)

    def get_serializer_context(self):
        context = super(CustomerFieldList, self).get_serializer_context()

        # Pass user uuid to serializer
        context['id'] = self.kwargs['pk']
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):

        try:
            value = request.data['value']
        except KeyError:
            return HttpResponse('Missing Parameter.',
                                status=status.HTTP_400_BAD_REQUEST)

        # Check if "value" of field is of type list
        if isinstance(value, list):
            request.data['value'] = value
        else:
            # If not not, put into a list
            if value is not None:
                request.data['value'] = [value]
            # If None, preserve None
            else:
                request.data['value'] = value

        # Perform serializer validation first, to check if all parameters were given
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = super().create(request, *args, **kwargs)

        return response


class CustomerFieldListVisibilitySetting(IsAuthenticatedMixin, generics.ListCreateAPIView):
    """
    read-update endpoint for user field list visibility settings
    1) View Customer Field List Visibility (GET)
    2) Update Customer Field List Visibility (POST)
    """

    queryset = CustomerFieldListVisibility.objects.all()
    serializer_class = CustomerFieldListVisibilitySerializer

    def get_queryset(self):

        # Get user
        user = get_object_or_404(User, id=self.kwargs['pk'])

        return CustomerFieldListVisibility.objects.filter(user=user)

    def create(self, request, *args, **kwargs):

        # empty data
        data: dict[str] = [3]

        # get user + data
        data = {
            'user': get_object_or_404(User, id=self.kwargs['pk']).id,
            'fieldname': request.data.get('fieldname', None),
            'visible': request.data.get('visible', None)
        }

        # get serializer
        serializer = self.get_serializer(data=data)

        # validate
        serializer.is_valid(raise_exception=True)

        # create
        self.perform_create(serializer)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
