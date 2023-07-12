# core/tests/core_test_case.py

import logging
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class LoggedInApiTestCase(APITestCase, URLPatternsTestCase):

    fixtures = [
        # Field Types
        "production/core-fieldtypes.json",
        # SuperUser
        "development/users-superuser.json",
        # Admin User Field List Visbility
        "development/users-superuser-userfieldlistvisibility.json",
        # Admin Customer Field List Visibility
        "development/customers-superuser-customerfieldlistvisibility.json",
        # Company Sites
        "development/core-companysites.json",
        # Users
        "development/users-users.json",
        # Field Meta Data (Users)
        "development/core-users-fieldmetadata.json",
        # Field Meta Data (Customers)
        "development/core-customers-fieldmetadata.json",
        # User Field Values
        "development/users-userfieldvalues.json",
        # User Field List Visbility
        "development/users-userfieldlistvisibility.json",
        # Customers
        "development/customers-customers.json",
        # Customer Field Values
        "development/customers-customerfieldvalues.json",
        # Customer Field List Visbility
        "development/customers-customerfieldlistvisibility.json"
    ]

    def setUp(self):
        # Set logger threshold to ERROR
        # so that 404 dont produce terminal output
        logger = logging.getLogger('django.request')
        logger.setLevel(logging.ERROR)

        # Perform login
        self.client = APIClient()

        admin = User.objects.get(username='admin')

        access_token = RefreshToken.for_user(admin).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token))
