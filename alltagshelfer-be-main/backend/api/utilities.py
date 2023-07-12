import datetime
# api/views.py
import logging
# django intern
from django.utils.timezone import make_aware

# rest_framework
from rest_framework import status, permissions

from rest_framework.exceptions import APIException

from rest_framework_simplejwt.tokens import AccessToken, TokenError
# Models
from .models import BlacklistedToken
from users.models import User, UserRoles


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class IsAuthenticated(permissions.IsAuthenticated):
    """
    checks if:
    1) token was given
    2) given token is valid (not blacklisted)
    3) user hasnt done logout-all
    """

    # https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
    def has_permission(self, request, view):

        # 1) Check if access token was given
        try:
            # Get 'HTTP_AUTHORIZATION'-Field in Header
            # As string
            access_token_str = str(
                request.META['HTTP_AUTHORIZATION'].split(' ')[1])
            # As token
            access_token = AccessToken(access_token_str)

        except KeyError as key_error:
            logging.error(key_error)
            raise GenericAPIException(
                detail="Unauthorized", status_code=401)
        except TokenError as token_error:
            logging.error(token_error)
            raise GenericAPIException(
                detail="Unauthorized", status_code=401)

        # 2) Check if token is a blacklisted token
        # (if no was found, error is raised)
        if BlacklistedToken.objects.filter(
                token=access_token_str).count() > 0:
            # return False
            raise GenericAPIException(detail="Unauthorized", status_code=401)

        # 3) Check if Token was created before invalidate_before date of user
        # Get creation date of token
        access_token_created_at = make_aware(
            datetime.datetime.fromtimestamp(access_token.payload['iat']))
        # Get invalidate_before date
        invalidate_before = User.objects.get(
            username=request.user).invalidate_before
        # Is invalidate_before set?
        if invalidate_before is not None:
            # Was the token created before invalidate_before?
            if access_token_created_at < invalidate_before:
                raise GenericAPIException(
                    detail="Unauthorized", status_code=401)

        return super().has_permission(request, view)


class IsSupervisor(IsAuthenticated):
    """
    Verifies that the role is either ADMIN, CEO or SUPERVISOR
    """

    def has_permission(self, request, view):

        # Call IsAuthenticated's has_permission first
        super().has_permission(request, view)

        role = request.user.role
        # 4) Check if user is at least Supervisor
        if role in [UserRoles.ADMIN, UserRoles.CEO, UserRoles.SUPERVISOR]:
            return True
        else:
            raise GenericAPIException(detail="Forbidden", status_code=403)


class IsUserOrSupervisor(IsAuthenticated):
    """
    Verifies that the role is either ADMIN, CEO or SUPERVISOR
    or the same user as the requested UUID
    """

    def has_permission(self, request, view):

        # Call IsAuthenticated's has_permission first
        super().has_permission(request, view)

        role = request.user.role
        id = view.kwargs['pk']
        # 4) Check if user is at least Supervisor
        if role in [UserRoles.ADMIN, UserRoles.CEO, UserRoles.SUPERVISOR]:
            return True
        # Or the user itself, calling his own UUID
        elif User.objects.get(id=id).id == id:
            return True
        else:
            raise GenericAPIException(detail="Forbidden", status_code=403)


class IsAuthenticatedMixin():
    permission_classes = [IsAuthenticated]


class IsSupervisorMixin():
    permission_classes = [IsSupervisor]


class IsUserOrSupervisorMixin():
    permission_classes = [IsUserOrSupervisor]
