# api/views.py

import datetime
# django intern
from django.utils.timezone import make_aware

# rest_framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
# SimpleJWT (Used for logout)

from rest_framework_simplejwt.tokens import AccessToken
# Models
from .utilities import IsAuthenticatedMixin
from .models import BlacklistedToken
from users.models import User
# Serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'customers': reverse('customer-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'fieldmeta': reverse('fieldmeta-list', request=request, format=format),
        'fieldtypes': reverse(
            'fieldtypes-list', request=request, format=format)
    })


class TokenBlacklistView(IsAuthenticatedMixin, APIView):
    """
    Blacklist access tokens
    """

    def post(self, request):

        try:

            # Get transmitted token
            token = AccessToken(
                str(request.META['HTTP_AUTHORIZATION'].split(' ')[1]))

            # Turn into time zone supported datetime
            expiration_datetime = make_aware(
                datetime.datetime.fromtimestamp(token.payload['exp']))

            # Store blacklisted token in database
            BlacklistedToken.objects.create(
                token=token, expiration_datetime=expiration_datetime)

            # Get user to token
            _ = User.objects.get(id=str(token.payload['user_id']))

            return Response(
                {"message": "logout successful."},
                status=status.HTTP_200_OK)
            # return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(request, status=status.HTTP_401_UNAUTHORIZED)


class TokenInvalidateAllView(IsAuthenticatedMixin, APIView):
    """
    Invalidate all active tokens by setting the invalidate_before tag
    """

    def post(self, request):

        # Get transmitted token
        token = AccessToken(
            str(request.META['HTTP_AUTHORIZATION'].split(' ')[1]))

        # Get user to token
        user = User.objects.get(id=str(token.payload['user_id']))

        # Invalidate all tokens, which have been created before "now"
        user.invalidate_before = make_aware(datetime.datetime.now())

        # Save user
        user.save()

        return Response(
            {"message": "logged out from all devices."},
            status=status.HTTP_200_OK)
