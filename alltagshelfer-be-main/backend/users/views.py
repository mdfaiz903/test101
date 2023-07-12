# users/views.py

import logging
import datetime
from typing import Callable, Union
# django intern
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
# rest_framework
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import User, UserFieldValue, UserFieldListVisibility
from core.models import FieldMetadata
from api.utilities import (IsUserOrSupervisorMixin, IsSupervisorMixin,
                           IsAuthenticatedMixin)


# Serializers
from users.serializers import (UserListCreateSerializer,
                               UserListCreateFullSerializer,
                               UserRetrieveUpdateDestroySerializer,
                               UserFieldValueSerializer,
                               UserFieldValueRetrieveUpdateDestroySerializer,
                               UserFieldListVisibilitySerializer,
                               ChangePasswordSerializer)


class UserRequestDetails(IsAuthenticatedMixin, APIView):
    """
    read endpoint to return details to requested user (if authenticated)
    1) Return User Fields (GET)
    """

    serializer_class = UserRetrieveUpdateDestroySerializer

    def get(self, request, format=None):
        instance = get_object_or_404(User, username=request.user)

        serializer = UserRetrieveUpdateDestroySerializer(
            instance=instance)

        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(UserRequestDetails, self).get_serializer_context()
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context


class UserList(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-write endport for a list of users
    1) List all Users (GET)
    2) Create new User (POST)
    """

    queryset = User.objects.filter(deleted=False)
    # serializer_class = UserListCreateFullSerializer
    serializer_classes: dict[str, Callable] = {
        'true': UserListCreateFullSerializer,
        'false': UserListCreateSerializer
    }

    def get_serializer_class(self) -> Union[
            UserListCreateSerializer,
            UserListCreateFullSerializer]:
        full_param = self.request.query_params.get('full')

        if not full_param:
            full_param = 'false'
        return self.serializer_classes[full_param]

    def get_serializer_context(self):
        context = super(UserList, self).get_serializer_context()
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context


class UserDetail(IsSupervisorMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    read-write-delete endpoint for a single user
    1) View User (GET)
    2) Update User (PUT)
    3) Delete User (DELETE)
    """

    queryset = User.objects.filter(deleted=False)
    serializer_class = UserRetrieveUpdateDestroySerializer

    def destroy(self, request, *args, **kwargs):

        # Get user or 404
        user = get_object_or_404(User, id=self.kwargs['pk'])

        # Delete user
        user.delete()

        return Response("Benutzer gelöscht", status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super(UserDetail, self).get_serializer_context()
        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context


class UserChangePassword(IsSupervisorMixin, generics.UpdateAPIView):
    """
    write endport for a single user
    1) Change Password of user (POST)
    """

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):

        # get the user
        user = self.get_object()

        # get the data from the request
        data = request.data

        # get the serializer with given user and data
        serializer = self.get_serializer(user, data=data)

        # check if given data is valid
        serializer.is_valid(raise_exception=True)

        # update password
        self.perform_update(serializer)

        # invalidate before (to avoid login with previously created tokens)
        user.invalidate_before = make_aware(datetime.datetime.now())

        # Save user
        user.save()

        # return Response(serializer.data)
        return Response(_('Passwort geändert'), status=status.HTTP_200_OK)


class UserFieldList(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-write endpoint for a list of fields for a specific user
    1) Get all Fields (GET)
    2) Create new Field for specified User (POST)
    """

    queryset = UserFieldValue.objects.all()
    serializer_class = UserFieldValueSerializer

    def get_queryset(self):
        # Get user
        user = get_object_or_404(User, id=self.kwargs['pk'])
        return UserFieldValue.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(UserFieldList, self).get_serializer_context()

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


class UserFieldDetail(IsSupervisorMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    read-write-delete endpoint for a single user field
    1) View User Field (GET)
    2) Update User Field (PUT)
    3) Delete User (DELETE)
    """

    queryset = UserFieldValue.objects.all()
    serializer_class = UserFieldValueRetrieveUpdateDestroySerializer

    def get_serializer_context(self):
        context = super(UserFieldDetail, self).get_serializer_context()

        # Pass user uuid to serializer
        context['id'] = self.kwargs['pk']

        # Pass field id to serializer
        context['field'] = self.kwargs['fieldpk']

        # Pass requesting user to serializer
        context['user'] = self.request.user
        return context

    def retrieve(self, request, *args, **kwargs):
        # Get user
        user = get_object_or_404(User, id=kwargs['pk'])
        # Get requested fieldmetadata
        field = FieldMetadata.objects.get(id=kwargs['fieldpk'])
        # Get fieldvalue
        instance = get_object_or_404(
            UserFieldValue, user=user, field=field)
        # instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Get user
        user = get_object_or_404(User, id=kwargs['pk'])
        # Get requested fieldmetadata
        field = FieldMetadata.objects.get(id=kwargs['fieldpk'])
        # Get fieldvalue
        instance = get_object_or_404(
            UserFieldValue, user=user, field=field)
        # instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
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

        # Get user
        user = get_object_or_404(User, id=kwargs['pk'])
        # Get requested fieldmetadata
        field = FieldMetadata.objects.get(id=kwargs['fieldpk'])
        # Get fieldvalue
        instance = get_object_or_404(
            UserFieldValue, user=user, field=field)
        # instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserFieldListVisibilitySetting(IsSupervisorMixin, generics.ListCreateAPIView):
    """
    read-update endpoint for user field list visibility settings
    1) View User Field List Visibility (GET)
    2) Update User Field List Visibility (POST)
    """

    queryset = UserFieldListVisibility.objects.all()
    serializer_class = UserFieldListVisibilitySerializer

    def get_queryset(self):

        # Get user
        user = get_object_or_404(User, id=self.kwargs['pk'])

        return UserFieldListVisibility.objects.filter(user=user)

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
