# users/tests/test_models.py

import copy
import logging
import datetime
from django.test import Client, TestCase
from django.urls import include, path, reverse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
# local
from core.constants import Kind
from core.tests.init_test_setup import LoggedInApiTestCase
from users.constants import UserCoreFields
from core.models import FieldMetadata
from users.models import (User, UserFieldValue,
                          build_username, UserFieldListVisibility)
from core.constants import UserRoles
from .constants import TEST_CAREGIVER, TEST_SUPERVISOR, TEST_CEO, TEST_ADMIN
from .constants import (TEST_CAREGIVER_OUTPUTS,
                        TEST_SUPERVISOR_OUTPUTS, TEST_CEO_OUTPUTS,
                        TEST_ADMIN_OUTPUTS)
from customers.models import CustomerFieldListVisibility
from customers.constants import CustomerCoreFields

# TESTED
# user-request (GET)
# user-list (GET, POST)
# user-detail (GET, PUT, DELETE)
# user-changepassword (POST)
# user-fields (GET, POST)
# user-field-detail (GET, PUT, DELETE)
# user-fields-visibility (GET, POST)


class UserRequestTests(LoggedInApiTestCase):
    # user-request (GET)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(UserRequestTests, self).setUp()

        # Specify url
        self.url = reverse(
            'user-request')

        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"users/tests/test_api.py" - UserRequestTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_correct_uuid(self):

        logging.info(
            '"users/tests/test_api.py" - UserRequestTests: Test correct UUID')

        # Check if correct uuid was returned
        self.assertEqual(
            self.response.data['id'],
            str(User.objects.get(username='admin').id))

    def test_fields_existence(self):

        logging.info(
            '"users/tests/test_api.py" - UserRequestTests: Test fields existence')

        # Make list from 'names' of fields
        field_names = []
        for val in self.response.data['field_values']:
            field_names.append(val['name'])

        # Check if every core field exists in response
        for field in UserCoreFields.get_fields():
            self.assertTrue(field['name'] in field_names)

        for field in FieldMetadata.objects.filter(kind=Kind.USER):
            self.assertTrue(field.name in field_names)

    def test_correct_values(self):

        logging.info(
            '"users/tests/test_api.py" - UserRequestTests: Test currect values')

        # Make dict from 'names' and 'values' of fields
        fields_response = {}
        for val in self.response.data['field_values']:
            fields_response[val['name']] = val['value']

        # get user
        user = User.objects.get(username='admin')

        # Check core fields
        for field in UserCoreFields.get_fields():

            # get current response
            response = fields_response[field['name']]

            if isinstance(getattr(user, field['name']), datetime.date):
                db_value = str(getattr(user, field['name']))
            else:
                db_value = getattr(user, field['name'])

            if field['name'] == 'last_login' or field['name'] == 'date_joined':
                # Convert db_value to datetime object
                db_value = parse_datetime(db_value)
                # Convert response to datetime object
                response = parse_datetime(fields_response[field['name']])

            self.assertEqual(
                db_value, response)

        for field in FieldMetadata.objects.filter(kind=Kind.USER):
            # get current response
            response = fields_response[field.name]

            # If response is None, no userfieldvalue shall be found
            if response is None:
                with self.assertRaises(UserFieldValue.DoesNotExist):
                    UserFieldValue.objects.get(field=field, user=user)

            # if not None, compare values
            else:
                db_value = UserFieldValue.objects.get(
                    field=field, user=user).value

                self.assertEqual(
                    db_value, response)


class UserListTests(LoggedInApiTestCase):
    # user-list (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):

        # Perform login
        super(UserListTests, self).setUp()
        # Specify url
        self.url = reverse('user-list')
        # Get response
        self.response = self.client.get(
            self.url, {'full': 'false'}, format='json')

        # Get response but with param=full
        self.response_full = self.client.get(
            self.url, {'full': 'true'}, format='json')

        # New User Data
        self.new_user_data = {
            "salutation": "Herr",
            "lastname": "Scholz",
            "firstname": "Olaf",
            "password": "besterKanzler2023",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "role": "CAREGIVER",
            "zip": "10000",
            "birthday": "1840-01-01"
        }

    def test_reaching_url(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test reaching URL')
        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        # Check status code
        self.assertEqual(self.response_full.status_code, status.HTTP_200_OK)

    def test_getting_user_list(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test getting list of users')
        # Get length of response data (should be as much as there are users)
        self.assertEqual(len(self.response.data), User.objects.all().count())

        # Check if all users (loaded via fixtures) were found
        # Get list of all users
        usernames = list(User.objects.all().values_list('username', flat=True))
        # Iterate over response list
        for data in self.response.data:
            # Iterate over usernames
            for username in usernames:
                if username == data['field_values'][3]['value']:
                    # If username was found, remove from list
                    usernames.remove(username)
        # No usernames shall be remaining
        self.assertEqual(len(usernames), 0)

        # Get number of core fields
        n_core_fields = len(UserCoreFields.get_fields())

        # Check if all user core fields were added
        self.assertEqual(len(self.response.data[0]['field_values']),
                         n_core_fields)

    def test_getting_user_list_full(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test getting list of users (full)')
        # Get length of response data (should be as much as there are users)
        self.assertEqual(len(self.response_full.data),
                         User.objects.all().count())

        # Check if all users (loaded via fixtures) were found
        # Get list of all users
        usernames = list(User.objects.all().values_list('username', flat=True))
        # Iterate over response list
        for data in self.response_full.data:
            # Iterate over usernames
            for username in usernames:
                if username == data['field_values'][3]['value']:
                    # If username was found, remove from list
                    usernames.remove(username)
        # No usernames shall be remaining
        self.assertEqual(len(usernames), 0)

        # Get number of core fields
        n_core_fields = len(UserCoreFields.get_fields())
        # Get number of created custom fields
        n_custom_fields = FieldMetadata.objects.filter(kind=Kind.USER).count()

        # Check if all user core fields were added
        self.assertEqual(len(self.response_full.data[0]['field_values']),
                         n_core_fields + n_custom_fields)

        # Check if visibility options are matching db_entries

    def test_creating_new_user(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test creating new User (with all required fields)')

        # Get number of userfieldvisibility and customerfieldvisibility items before adding user
        n_userfieldlistvisibilityitems_before = UserFieldListVisibility.objects.all().count()
        n_customerfieldlistvisibilityitems_before = CustomerFieldListVisibility.objects.all().count()

        # Perform POST Request
        response = self.client.post(
            self.url, self.new_user_data, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if user was added to users
        self.assertEqual(User.objects.all().count(), 5)

        new_user = User.objects.all().latest('date_joined')

        # Check if all specified fields were set
        self.assertEqual(new_user.salutation, 'Herr')
        self.assertEqual(new_user.lastname, 'Scholz')
        self.assertEqual(new_user.firstname, 'Olaf')
        self.assertEqual(new_user.username, 'olafscholz')
        self.assertEqual(new_user.street, 'irgendwostr.')
        self.assertEqual(new_user.house_number, '99')
        self.assertEqual(new_user.city, 'Berlin')
        self.assertEqual(new_user.role, UserRoles.CAREGIVER)
        self.assertEqual(new_user.zip, '10000')
        self.assertEqual(new_user.birthday, datetime.date(1840, 1, 1))

        # Check if userfieldlistvisibility items were added
        userfieldslistvisibilities = list(UserFieldListVisibility.objects.filter(
            user=new_user).values_list('fieldname', flat=True))

        corefields_full = UserCoreFields.get_fields()
        customfields = FieldMetadata.objects.filter(
            kind=Kind.USER).values_list('name', flat=True)

        # generate list of field names
        corefields = []
        for field in corefields_full:
            corefields.append(field['name'])
        fields = corefields + list(customfields)

        # Get number of userfieldvisibility and customerfieldvisibility items after adding user
        n_userfieldlistvisibilityitems_after = UserFieldListVisibility.objects.all().count()

        self.assertEqual(n_userfieldlistvisibilityitems_after -
                         n_userfieldlistvisibilityitems_before, len(fields))

        for field in fields:
            for userfieldvisibility in userfieldslistvisibilities:
                if field == userfieldvisibility:
                    userfieldslistvisibilities.remove(field)

            # No field shall be remaining
        self.assertEqual(len(userfieldslistvisibilities), 0)

        # Check customerfieldlistvisibility items were added
        customerfieldslistvisibilities = list(CustomerFieldListVisibility.objects.filter(
            user=new_user).values_list('fieldname', flat=True))

        corefields_full = CustomerCoreFields.get_fields()
        customfields = FieldMetadata.objects.filter(
            kind=Kind.CUSTOMER).values_list('name', flat=True)

        # generate list of field names
        corefields = []
        for field in corefields_full:
            corefields.append(field['name'])
        fields = corefields + list(customfields)

        n_customerfieldlistvisibilityitems_after = CustomerFieldListVisibility.objects.all().count()
        self.assertEqual(n_customerfieldlistvisibilityitems_after -
                         n_customerfieldlistvisibilityitems_before, len(fields))

        for field in fields:
            for customerfieldslistvisibility in customerfieldslistvisibilities:
                if field == customerfieldslistvisibility:
                    customerfieldslistvisibilities.remove(field)

            # No field shall be remaining
        self.assertEqual(len(customerfieldslistvisibilities), 0)

    def test_creating_new_user_with_wrong_fields(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test creating new User (with wrong data)')

        # New User Data
        wrong_user_data = {
            "salutation": "abcd",
            "lastname": "Scholz",
            "firstname": "Olaf",
            "password": "besterKanzler2023",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "role": "CAREGIVER",
            "zip": "10000",
            "birthday": "falsch"
        }

        # Check if visibility entries are the same before and after trying to add the user
        n_userfieldlistvisibilityitems_before = UserFieldListVisibility.objects.all().count()
        n_customerfieldlistvisibilityitems_before = CustomerFieldListVisibility.objects.all().count()

        response = self.client.post(
            self.url, wrong_user_data, format='json')

        n_userfieldlistvisibilityitems_after = UserFieldListVisibility.objects.all().count()
        n_customerfieldlistvisibilityitems_after = CustomerFieldListVisibility.objects.all().count()

        self.assertEqual(n_customerfieldlistvisibilityitems_after -
                         n_customerfieldlistvisibilityitems_before, 0)
        self.assertEqual(n_userfieldlistvisibilityitems_after -
                         n_userfieldlistvisibilityitems_before, 0)

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Check if customer was added to customers
        self.assertEqual(User.objects.all().count(), 4)

    def test_creating_new_user_with_incomplete_fields(self):
        logging.info(
            '"users/tests/test_api.py" - UserListTests: Test creating new User (with incomplete data)')

        list_of_required_fields = ['salutation',
                                   'lastname',
                                   'firstname',
                                   'street',
                                   'house_number',
                                   'city',
                                   'zip',
                                   'birthday']

        # Test for each field missing

        for field in list_of_required_fields:
            incomplete_data = copy.deepcopy(self.new_user_data)

            # Delete field
            del incomplete_data[field]

            # Check if visibility entries are the same before and after trying to add the user
            n_userfieldlistvisibilityitems_before = UserFieldListVisibility.objects.all().count()
            n_customerfieldlistvisibilityitems_before = CustomerFieldListVisibility.objects.all().count()

            response = self.client.post(
                self.url, incomplete_data, format='json')

            n_userfieldlistvisibilityitems_after = UserFieldListVisibility.objects.all().count()
            n_customerfieldlistvisibilityitems_after = CustomerFieldListVisibility.objects.all().count()

            self.assertEqual(n_customerfieldlistvisibilityitems_after -
                             n_customerfieldlistvisibilityitems_before, 0)
            self.assertEqual(n_userfieldlistvisibilityitems_after -
                             n_userfieldlistvisibilityitems_before, 0)
            # Check status code
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)

        # Check if user was added to users
        self.assertEqual(User.objects.all().count(), 4)


class UserDetailTests(LoggedInApiTestCase):
    # user-detail (GET, PUT, DELETE)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(UserDetailTests, self).setUp()

        # Get primary key of of user
        self.pk = User.objects.get(username='martinmueller').pk

        # Specify url
        self.url = reverse(
            'user-detail', args=[self.pk])
        # Get response
        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_getting_user(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test getting user')

        # Get response data
        data = self.response.data

        # Check if not empty
        self.assertNotEqual(data, [])

        # Check id
        self.assertEqual(
            str(data['id']), '735dc5b8-b3d2-4f64-a4c1-9f34bada291a')

        # Store field values in data
        data = self.response.data['field_values']

        # Check values
        for field in data:
            if field['name'] == 'last_login':
                self.assertEqual(
                    field['value'], None)
            elif field['name'] == 'date_joined':
                self.assertEqual(
                    field['value'], '2023-04-03 11:58:01+00:00')
            elif field['name'] == 'username':
                self.assertEqual(
                    field['value'], 'martinmueller')
            elif field['name'] == 'salutation':
                self.assertEqual(
                    field['value'], 'Herr')
            elif field['name'] == 'lastname':
                self.assertEqual(
                    field['value'], 'Müller')
            elif field['name'] == 'firstname':
                self.assertEqual(
                    field['value'], 'Martin')
            elif field['name'] == 'street':
                self.assertEqual(
                    field['value'], 'Wehrstraße')
            elif field['name'] == 'house_number':
                self.assertEqual(
                    field['value'], '139')
            elif field['name'] == 'city':
                self.assertEqual(
                    field['value'], 'Oberhausen')
            elif field['name'] == 'zip':
                self.assertEqual(
                    field['value'], '46047')
            elif field['name'] == 'address_addition':
                self.assertEqual(
                    field['value'], None)
            elif field['name'] == 'phone_mobile':
                self.assertEqual(
                    field['value'], '0173123456789')
            elif field['name'] == 'phone_house':
                self.assertEqual(
                    field['value'], '0208123456789')
            elif field['name'] == 'birthday':
                self.assertEqual(
                    field['value'], '1985-08-15')
            elif field['name'] == 'email':
                self.assertEqual(
                    field['value'], None)
            elif field['name'] == 'comments':
                self.assertEqual(
                    field['value'], '')
            elif field['name'] == 'role':
                self.assertEqual(
                    field['value'], 'CAREGIVER')
            elif field['name'] == 'companysite':
                self.assertEqual(
                    field['value'], '1')

        # Get number of core fields
        n_core_fields = len(UserCoreFields.get_fields())
        # Get number of created custom fields
        n_custom_fields = FieldMetadata.objects.filter(kind=Kind.USER).count()

        # Check if all user core fields were added
        self.assertEqual(len(self.response.data['field_values']),
                         n_core_fields + n_custom_fields)

    def test_getting_nonexistent_user(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test getting nonexistent user')

        url_nonexistent = reverse(
            'user-detail', args=['735dc5b8-b3d2-4f64-a4c1-1134bada291a'])

        response_nonexistent = self.client.get(
            url_nonexistent, {}, format='json')

        # Check status code
        self.assertEqual(response_nonexistent.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_getting_deleted_user(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test getting deleted user')

        # Delete user
        User.objects.get(
            id='735dc5b8-b3d2-4f64-a4c1-9f34bada291a').delete()

        url_deleted = reverse(
            'customer-detail', args=['735dc5b8-b3d2-4f64-a4c1-9f34bada291a'])

        response_deleted = self.client.get(
            url_deleted, {}, format='json')

        # Check status code
        self.assertEqual(response_deleted.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_updating_user(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test updating user')

        # Update User Data
        self.update_user_data = {
            "salutation": "Frau",
            "lastname": "Scholz",
            "firstname": "Olaf",
            "password": "besterKanzler2023",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "role": "CAREGIVER",
            "zip": "10000",
            "birthday": "1840-01-01"
        }

        # Update salutation
        response = self.client.put(
            self.url, self.update_user_data, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        # Check if new salutation was set
        self.assertEqual(User.objects.get(
            username='martinmueller').salutation, 'Frau')

    def test_deleting_user(self):

        logging.info(
            '"users/tests/test_api.py" - UserDetailTests: Test deleting user')

        # Delete user
        response = self.client.delete(self.url, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

        # User shall still be existent
        # Check if user is not listed anymore when filtering deleted
        self.assertFalse(User.objects.filter(
            username='martinmueller', deleted=False).exists())

        # But with deleted-tag = true
        self.assertEqual(User.objects.get(
            username='martinmueller').deleted, True)

        # Check correct deleted_at timestamp
        self.assertEqual(User.objects.get(
            username='martinmueller').deleted_at.date(),
            datetime.datetime.today().date())


class UserChangePasswordTests(LoggedInApiTestCase):
    # user-changepassword (POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(UserChangePasswordTests, self).setUp()

        # Get primary key of of admin
        self.pk_admin = User.objects.get(username='admin').pk

        # Specify url
        self.url_admin = reverse(
            'user-changepassword', args=[self.pk_admin])

        # Get primary key of of admin
        self.pk_caregiver = User.objects.get(username='jacquelineschneider').pk

        # Specify url
        self.url_caregiver = reverse(
            'user-changepassword', args=[self.pk_caregiver])

    # Get primary key of of admin
        self.pk_other_caregiver = User.objects.get(
            username='martinmueller').pk

        # Specify url
        self.url_other_caregiver = reverse(
            'user-changepassword', args=[self.pk_caregiver])

    def test_changing_own_password_as_supervisor(self):
        logging.info(
            '"users/tests/test_api.py" - UserChangePasswordTests: Test changing own password as supervisor')

        # Login with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'admin',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Change password
        self.response = self.client.put(
            self.url_admin, {'password': 'newpassword1234',
                             'password2': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Login with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'admin',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # Login with new password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'admin',
                                      'password': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_changing_other_password_as_supervisor(self):
        logging.info(
            '"users/tests/test_api.py" - UserChangePasswordTests: Test changing other password as supervisor')

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Change password
        self.response = self.client.put(
            self.url_caregiver, {'password': 'newpassword1234',
                                 'password2': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # Login as caregiver with new password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_changing_password_with_wrong_data(self):
        logging.info(
            '"users/tests/test_api.py" - UserChangePasswordTests: Test changing password with wrong data')

        # Change password without giving any password
        self.response = self.client.put(
            self.url_admin, {}, format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Change password with only one password
        self.response = self.client.put(
            self.url_admin, {'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Change password with two different passwords
        self.response = self.client.put(
            self.url_admin, {'password': 'alltagshelfer1234',
                             'password2': 'someotherpassword'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_changing_own_password_as_caregiver(self):
        logging.info(
            '"users/tests/test_api.py" - UserChangePasswordTests: Test changing own password as caregiver')

        # Perform login
        client_caregiver = APIClient()

        caregiver = User.objects.get(username='jacquelineschneider')

        access_token = RefreshToken.for_user(caregiver).access_token

        client_caregiver.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token))

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Change password
        self.response = self.client.put(
            self.url_caregiver, {'password': 'newpassword1234',
                                 'password2': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # Login as caregiver with new password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'jacquelineschneider',
                                      'password': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_changing_other_password_as_caregiver(self):
        logging.info(
            '"users/tests/test_api.py" - UserChangePasswordTests: Test changing other password as caregiver')

        # Perform login
        client_caregiver = APIClient()

        caregiver = User.objects.get(username='jacquelineschneider')

        access_token = RefreshToken.for_user(caregiver).access_token

        client_caregiver.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(access_token))

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'martinmueller',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Change password
        self.response = self.client.put(
            self.url_other_caregiver, {'password': 'newpassword1234',
                                       'password2': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Login as caregiver with previous password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'martinmueller',
                                      'password': 'alltagshelfer1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

        # Login as caregiver with new password
        self.response = self.client.post(
            reverse('token-obtain'), {'username': 'martinmueller',
                                      'password': 'newpassword1234'},
            format='json')
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class UserFieldsListTests(LoggedInApiTestCase):
    # user-fields (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(UserFieldsListTests, self).setUp()

        # Get primary key of martinmueller
        self.pk_has_fields = User.objects.get(username='martinmueller').pk

        # Specify url
        self.url_has_fields = reverse(
            'user-fields', args=[self.pk_has_fields])

        # Get response
        self.response_has_fields = self.client.get(
            self.url_has_fields, {}, format='json')

        # Get primary key of farisabdelrehim (has no fields yet)
        self.pk = User.objects.get(username='farisabdelrehim').pk

        # Specify url
        self.url = reverse(
            'user-fields', args=[self.pk])

        # Get response
        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_all_user_fields(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test getting all user fields')

        # Check if four fields were returned
        self.assertTrue(len(self.response_has_fields.data) == 4)

        # Check if all user field values (loaded via fixtures) were found
        # Get list of all user field values
        userfieldvaluetitles = list(
            UserFieldValue.objects.all().values_list('field__title',
                                                     flat=True))
        # Iterate over response list
        for data in self.response_has_fields.data:
            # Iterate over userfieldvaluetitles
            for userfieldvaluetitle in userfieldvaluetitles:
                if userfieldvaluetitle == data['title']:

                    # If userfieldvalue was found, remove from list
                    userfieldvaluetitles.remove(userfieldvaluetitle)
        # Only one userfieldvalue shall remain
        self.assertEqual(len(userfieldvaluetitles), 1)

    def test_add_and_update_user_fields(self):
        """
        Fieldtypes
        Boolean - Checkbox
        Integer - Input
        Integer - Select
        Integer - Multiselect
        Float - Input
        Float - Select
        Float - Multiselect
        String - Input
        String - Select
        String - Multiselect
        Date - Date
        """
        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test adding and updating user field values')

        user = User.objects.get(username='farisabdelrehim')

        # Adding
        values = [
            "true",                     # Boolean-Checkbox
            "5",                        # Integer-Input
            "3",                        # Integer-Select
            "2",                        # Integer-Multiselect
            "1.76",                     # Float-Input
            "12.50",                    # Float-Select
            "2.5",                      # Float-Multiselect
            "Fachoberschulreife",       # String-Input
            "Teilzeit",                 # String-Select
            ["Betreuung", "Einkaufen"],  # String-Multiselect
            "2019-09-04"                # Date-Date
        ]

        id = 0
        for value in values:
            id += 1
            field = FieldMetadata.objects.get(id=id)
            # Add user field
            response_add = self.client.post(
                self.url, {"field": field.id, "value": value}, format='json')

            # Check status code
            self.assertEqual(response_add.status_code, status.HTTP_201_CREATED)

            # Check if farisabdelrehim has id FieldValues now
            self.assertEqual(UserFieldValue.objects.filter(
                user=user).count(), id)

            # Convert value to list, to compare to db entry (which is arrayfield always)
            if isinstance(value, list):
                pass
            else:
                value = [value]

            # Check if correct value was stored in field
            self.assertEqual(UserFieldValue.objects.get(
                user=user, field=field).value, value)

        # Store number of fields to make sure,
        # number of fields remain the same when updating
        n_fields = id

        # Updating
        values_new = [
            "false",                    # Boolean-Checkbox
            "1",                        # Integer-Input
            "5",                        # Integer-Select
            "3",                        # Integer-Multiselect
            "1.91",                     # Float-Input
            "27.50",                    # Float-Select
            ["2.5", "3.5"],             # Float-Multiselect
            "Hauptschulabschluss",      # String-Input
            "Minijob",                  # String-Select
            "Betreuung",                # String-Multiselect
            "2019-09-05"                # Date-Date
        ]

        id = 0
        for value in values_new:
            id += 1
            field = FieldMetadata.objects.get(id=id)
            # Add user field
            response_update = self.client.post(
                self.url, {"field": field.id, "value": value}, format='json')

            # Check status code
            self.assertEqual(response_update.status_code,
                             status.HTTP_201_CREATED)

            # Check if farisabdelrehim has still all fields
            self.assertEqual(UserFieldValue.objects.filter(
                user=user).count(), n_fields)

            # Convert value to list, to compare to db entry (which is arrayfield always)
            if isinstance(value, list):
                pass
            else:
                value = [value]

            # Check if correct value was stored in field
            self.assertEqual(UserFieldValue.objects.get(
                user=user, field=field).value, value)

    def test_add_user_field_nonexistent_id(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test adding user field specifying a nonexistent field')

        # Add user field
        response_add = self.client.post(
            self.url, {"field": FieldMetadata.objects.all().count()+1, "value": 'test'}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_add_user_field_missing_required_param(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test adding user field missing a required parameter (value)')

        # Try adding user field without value parameter
        response_add = self.client.post(
            self.url, {"field": 1}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Try adding user field without field parameter
        response_add = self.client.post(
            self.url, {"value": 1}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_add_user_field_with_datatype_mismatch(self):
        """
        Fieldtypes
        Boolean - Checkbox
        Integer - Input
        Integer - Select
        Integer - Multiselect
        Float - Input
        Float - Select
        Float - Multiselect
        String - Input
        String - Select
        String - Multiselect
        Date - Date
        """
        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test adding user field with wrong datatypes')

        user = User.objects.get(username='farisabdelrehim')

        values = [
            "hallo",                        # Boolean-Checkbox
            "true",                         # Integer-Input
            "3.5",                          # Integer-Select
            ["2.4", "3.2"],                 # Integer-Multiselect
            "hallo",                        # Float-Input
            "Hallo",                        # Float-Select
            ["hallo", "hallo2"],            # Float-Multiselect
            "hallo"                         # Date-Date
        ]

        id = 0
        for value in values:
            id += 1

            # Skip the string fields
            if id in [8, 9, 10]:
                pass
            else:
                field = FieldMetadata.objects.get(id=id)
                # Add user field
                response_add = self.client.post(
                    self.url, {"field": field.id, "value": value}, format='json')

                # Check status code
                self.assertEqual(response_add.status_code,
                                 status.HTTP_400_BAD_REQUEST)

                # Check if farisabdelrehim has still 0 FieldValues
                self.assertEqual(UserFieldValue.objects.filter(
                    user=user).count(), 0)

    def test_add_user_field_with_wrong_Select_selections(self):
        """
        Fieldtypes
        Integer - Select
        Integer - Multiselect
        Float - Select
        Float - Multiselect
        String - Select
        String - Multiselect
        """
        logging.info(
            '"users/tests/test_api.py" - UserFieldsListTests: Test adding user field with wrong Select selections')

        user = User.objects.get(username='farisabdelrehim')

        values = [
            "6",                                # Integer-Select
            ["3", "4"],                         # Integer-Multiselect
            "11.50",                            # Float-Select
            ["3.5", "7.2"],                     # Float-Multiselect
            "1-Euro-Job",                       # String-Select
            ["Gassi Gehen", "Einkaufen"]        # String-Multiselect
        ]

        id = -1
        field_ids = [3, 4, 6, 7, 9, 10]
        for value in values:
            id += 1
            field = FieldMetadata.objects.get(id=field_ids[id])
            # Add user field
            response_add = self.client.post(
                self.url, {"field": field.id, "value": value}, format='json')
            # Check status code
            self.assertEqual(response_add.status_code,
                             status.HTTP_400_BAD_REQUEST)

            # Check if farisabdelrehim has still 0 FieldValues
            self.assertEqual(UserFieldValue.objects.filter(
                user=user).count(), 0)


class UserFieldsDetailTest(LoggedInApiTestCase):
    # user-field-detail (GET, PUT, DELETE)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_get_specfic_field_of_user(self):
        logging.info(
            '"users/tests/test_api.py" - UserFieldsDetailTest: Test getting specific field of user')

    def test_update_user_field(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsDetailTest: Test updating user field')

        pass

    def test_delete_field(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsDetailTest: Test deleting user field')
        pass


class UserFieldsListVisibilityListTest(LoggedInApiTestCase):
    # user-fields-visibility (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(UserFieldsListVisibilityListTest, self).setUp()

        # Get primary key of admin
        self.pk = User.objects.get(username='admin').pk

        # Specify url
        self.url = reverse(
            'user-fields-visibility', args=[self.pk])

        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListVisibilityListTest: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_getting_visibility_list(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListVisibilityListTest: Test getting visibility preferences')

        # Check if visibility options are matching db_entries
        for field in UserCoreFields.get_fields():
            visible = UserFieldListVisibility.objects.get(fieldname=field['name'],
                                                          user=User.objects.get(username='admin')).visible

        # Make dict from 'names' and 'values' of visbility fields
        userfieldlistvisibilities = {}
        # core fields
        for field in UserCoreFields.get_fields():
            userfieldlistvisibilities[field['name']] = UserFieldListVisibility.objects.get(fieldname=field['name'],
                                                                                           user=User.objects.get(username='admin')).visible
        # custom fields
        for field in FieldMetadata.objects.filter(kind=Kind.USER):
            userfieldlistvisibilities[field.name] = UserFieldListVisibility.objects.get(fieldname=field.name,
                                                                                        user=User.objects.get(username='admin')).visible
        # check correct number of entries
        n_core_fields = len(UserCoreFields.get_fields())
        n_custom_fields = len(FieldMetadata.objects.filter(kind=Kind.USER))

        self.assertEqual(len(self.response.data),
                         n_core_fields + n_custom_fields)

        for data in self.response.data:
            self.assertEqual(
                userfieldlistvisibilities[data['fieldname']], data['visible'])

    def test_changing_visibility_setting(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListVisibilityListTest: Test changing visibility preferences')

        # set visibility of salutation to false
        self.response = self.client.post(
            self.url, {'fieldname': 'salutation', 'visible': False}, format='json')

        self.assertFalse(UserFieldListVisibility.objects.get(
            fieldname='salutation',
            user=User.objects.get(username='admin')).visible)

    def test_changing_visibility_setting_missing_param(self):

        logging.info(
            '"users/tests/test_api.py" - UserFieldsListVisibilityListTest: Test changing visibility preferences missing params')

        # set visibility of salutation to false
        self.response = self.client.post(
            self.url, {'fieldname': 'salutation'}, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertTrue(UserFieldListVisibility.objects.get(
            fieldname='salutation',
            user=User.objects.get(username='admin')).visible)

        # set visibility of salutation to false
        self.response = self.client.post(
            self.url, {'visible': False}, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertEqual(True, UserFieldListVisibility.objects.get(
            fieldname='salutation',
            user=User.objects.get(username='admin')).visible)
