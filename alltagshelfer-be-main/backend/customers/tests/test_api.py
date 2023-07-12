# customers/tests/test_models.py

import copy
import logging
import datetime
from django.test import Client, TestCase
from django.urls import include, path, reverse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from customers.models import CustomerFieldListVisibility
# local
from core.constants import Kind
from core.tests.init_test_setup import LoggedInApiTestCase
from customers.constants import CustomerCoreFields
from core.models import FieldMetadata
from users.models import User
from customers.models import Customer, CustomerFieldValue

# TESTED
# customer-list (GET, POST)
# customer-detail (GET, PUT, DELETE)
# customer-fields (GET, POST)
# customer-fields-visibility (GET, POST)


class CustomerListTests(LoggedInApiTestCase):
    # customer-list (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):

        # Perform login
        super(CustomerListTests, self).setUp()
        # Specify url
        self.url = reverse('customer-list')
        # Get response
        self.response = self.client.get(
            self.url, {'full': 'false'}, format='json')

        # Get response but with param=full
        self.response_full = self.client.get(
            self.url, {'full': 'true'}, format='json')

        # New Customer Data
        self.new_customer_data = {
            "salutation": "Herr",
            "lastname": "Scholz",
            "firstname": "Olaf",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "zip": "10000",
            "birthday": "1840-01-01"
        }

    def test_reaching_url(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test reaching URL')
        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        # Check status code
        self.assertEqual(self.response_full.status_code,
                         status.HTTP_200_OK)

    def test_getting_customer_list(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test getting list of customers')
        # Get length of response data (should be as much as there are customers)
        self.assertEqual(len(self.response.data),
                         Customer.objects.all().count())

        # Check if all customers (loaded via fixtures) were found
        # Get list of all customers
        ids = list(Customer.objects.all(
        ).values_list('id', flat=True))
        # Iterate over response list
        for data in self.response.data:
            # Iterate over ids
            for id in ids:
                if str(id) == data['id']:
                    # If username was found, remove from list
                    ids.remove(id)
        # No id shall remain
        self.assertEqual(len(ids), 0)

        # Get number of core fields
        n_core_fields = len(CustomerCoreFields.get_fields())

        # Check if all customer core fields were added
        self.assertEqual(len(self.response.data[0]['field_values']),
                         n_core_fields)

    def test_getting_customer_list_full(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test getting list of customers (full)')
        # Get length of response data (should be as much as there are customers)
        self.assertEqual(len(self.response_full.data),
                         Customer.objects.all().count())

        # Check if all customers (loaded via fixtures) were found
        # Get list of all customers
        ids = list(Customer.objects.all(
        ).values_list('id', flat=True))
        # Iterate over response list
        for data in self.response.data:
            # Iterate over ids
            for id in ids:
                if str(id) == data['id']:
                    # If username was found, remove from list
                    ids.remove(id)
        # No id shall remain
        self.assertEqual(len(ids), 0)

        # Get number of core fields
        n_core_fields = len(CustomerCoreFields.get_fields())
        # Get number of custom fields
        n_custom_fields = FieldMetadata.objects.filter(
            kind=Kind.CUSTOMER).count()

        # Check if all customer custom fields were added
        self.assertEqual(len(self.response_full.data[0]['field_values']),
                         n_core_fields + n_custom_fields)

    def test_creating_new_customer(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test creating new Customer (with all required fields)')

        # Perform POST Request
        response = self.client.post(
            self.url, self.new_customer_data, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if customer was added to customers
        self.assertEqual(Customer.objects.all().count(), 3)

        new_customer = Customer.objects.all().latest('created_at')

        # Check if all specified fields were set
        self.assertEqual(new_customer.salutation, 'Herr')
        self.assertEqual(new_customer.lastname, 'Scholz')
        self.assertEqual(new_customer.firstname, 'Olaf')
        self.assertEqual(new_customer.street, 'irgendwostr.')
        self.assertEqual(new_customer.house_number, '99')
        self.assertEqual(new_customer.city, 'Berlin')
        self.assertEqual(new_customer.zip, '10000')
        self.assertEqual(new_customer.birthday, datetime.date(1840, 1, 1))

    def test_creating_new_customer_with_wrong_fields(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test creating new Customer (with wrong data)')

        # New Customer Data
        wrong_customer_data = {
            "salutation": "abcd",
            "lastname": "Scholz",
            "firstname": "Olaf",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "zip": "10000",
            "birthday": "falsch"
        }

        response = self.client.post(
            self.url, wrong_customer_data, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Check if customer was added to customers
        self.assertEqual(Customer.objects.all().count(), 2)

    def test_creating_new_customer_with_incomplete_fields(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerListTests: Test creating new Customer (with incomplete data)')

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
            incomplete_data = copy.deepcopy(self.new_customer_data)

            # Delete field
            del incomplete_data[field]

            response = self.client.post(
                self.url, incomplete_data, format='json')

            # Check status code
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)

            # Check if customer was added to customers
            self.assertEqual(Customer.objects.all().count(), 2)


class CustomerDetailTests(LoggedInApiTestCase):
    # customer-detail (GET, PUT, DELETE)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(CustomerDetailTests, self).setUp()

        # Get primary key of of customer
        self.pk = Customer.objects.get(lastname='Friedrichs').pk

        # Specify url
        self.url = reverse(
            'customer-detail', args=[self.pk])
        # Get response
        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_getting_customer(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test getting customers')

        # Get response data
        data = self.response.data

        # Check if not empty
        self.assertNotEqual(data, [])

        # Check id
        self.assertEqual(
            str(data['id']), '4098ee00-be32-486e-aa4a-bb6af716ca97')

        # Store field values in data
        data = self.response.data['field_values']

        # Check values
        for field in data:
            if field['name'] == 'lastname':
                self.assertEqual(
                    field['value'], 'Friedrichs')
            elif field['name'] == 'firstname':
                self.assertEqual(
                    field['value'], 'Sabine')
            elif field['name'] == 'street':
                self.assertEqual(
                    field['value'], 'Heerstraße')
            elif field['name'] == 'house_number':
                self.assertEqual(
                    field['value'], '26')
            elif field['name'] == 'city':
                self.assertEqual(
                    field['value'], 'Dinslaken')
            elif field['name'] == 'zip':
                self.assertEqual(
                    field['value'], '46535')
            elif field['name'] == 'address_addition':
                self.assertEqual(
                    field['value'], 'zweite Etage')
            elif field['name'] == 'phone_mobile':
                self.assertEqual(
                    field['value'], '01521234512345')
            elif field['name'] == 'phone_house':
                self.assertEqual(
                    field['value'], None)
            elif field['name'] == 'birthday':
                self.assertEqual(
                    field['value'], '1959-04-02')
            elif field['name'] == 'email':
                self.assertEqual(
                    field['value'], None)
            elif field['name'] == 'comments':
                self.assertEqual(
                    field['value'], '')

        # Get number of core fields
        n_core_fields = len(CustomerCoreFields.get_fields())
        # Get number of custom fields
        n_custom_fields = FieldMetadata.objects.filter(
            kind=Kind.CUSTOMER).count()

        # Check if all customer custom fields were added
        self.assertEqual(len(self.response.data['field_values']),
                         n_core_fields + n_custom_fields)

    def test_getting_nonexistent_customer(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test getting nonexistent customer')

        url_nonexistent = reverse(
            'user-detail', args=['735dc5b8-b3d2-4f64-a4c1-1134bada291a'])

        response_nonexistent = self.client.get(
            url_nonexistent, {}, format='json')

        # Check status code
        self.assertEqual(response_nonexistent.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_getting_deleted_customer(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test getting deleted customer')

        # Delete customer
        Customer.objects.get(
            id='4098ee00-be32-486e-aa4a-bb6af716ca97').delete()

        url_deleted = reverse(
            'customer-detail', args=['4098ee00-be32-486e-aa4a-bb6af716ca97'])

        response_deleted = self.client.get(
            url_deleted, {}, format='json')

        # Check status code
        self.assertEqual(response_deleted.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_updating_customer(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test updating customer')

        # Update Customer Data
        self.update_customer_data = {
            "salutation": "Frau",
            "lastname": "Hermanns",
            "firstname": "Olaf",
            "password": "besterKanzler2023",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "zip": "10000",
            "birthday": "1840-01-01"
        }

        # Update salutation
        response = self.client.put(
            self.url, self.update_customer_data, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        # Check if new lastname was set
        self.assertEqual(Customer.objects.get(
            pk=self.pk).lastname, 'Hermanns')

    def test_updating_customer_with_wrong_fields(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test updating customer (with wrong data)')

        # Update Customer Data
        self.update_customer_data = {
            "salutation": "Herr",
            "lastname": "Hermanns",
            "firstname": "Olaf",
            "password": "besterKanzler2023",
            "street": "irgendwostr.",
            "house_number": "99",
            "city": "Berlin",
            "zip": "10000",
            "birthday": "falsch"
        }

        # Update customer
        response = self.client.put(
            self.url, self.update_customer_data, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_updating_customer_with_incomplete_fields(self):
        logging.info(
            '"customers/tests/test_api.py" - CustomerDetailTests: Test updating customer (with incomplete data)')

        # Update Customer Data
        self.update_customer_data = {
            "salutation": "Herr"
        }

        # Update customer
        response = self.client.put(
            self.url, self.update_customer_data, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_deleting_customer(self):

        logging.info(
            '"customers/tests/test_api.py" - UserDetailTests: Test deleting customer')

        # Delete customers
        response = self.client.delete(self.url, format='json')

        # Check status code
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

        # Customer shall still be existent
        # Check if user is not listed anymore when filtering deleted
        self.assertFalse(Customer.objects.filter(
            lastname='Friedrichs', deleted=False).exists())

        # But with deleted-tag = true
        self.assertEqual(Customer.objects.get(
            lastname='Friedrichs').deleted, True)

        # Check correct deleted_at timestamp
        self.assertEqual(Customer.objects.get(
            lastname='Friedrichs').deleted_at.date(),
            datetime.datetime.today().date())


class CustomerFieldsListTests(LoggedInApiTestCase):
    # customer-fields (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(CustomerFieldsListTests, self).setUp()

        # Get primary key of of customer who has fields
        self.pk_has_fields = Customer.objects.get(lastname='Friedrichs').pk

        # Specify url
        self.url_has_fields = reverse(
            'customer-fields', args=[self.pk_has_fields])

        # Get response
        self.response_has_fields = self.client.get(
            self.url_has_fields, {}, format='json')

        # Get primary key of customer who has no fields yet
        self.pk = Customer.objects.get(lastname='Duck').pk

        # Specify url
        self.url = reverse(
            'customer-fields', args=[self.pk])

        # Get response
        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerFieldsListTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_all_customer_fields(self):

        logging.info(
            '"users/tests/test_api.py" - CustomerFieldsListTests: Test getting all customer fields')

        # Check if two fields were returned
        self.assertTrue(len(self.response_has_fields.data) == 2)

        # Check if all customer field values (loaded via fixtures) were found
        # Get list of all user fields
        customerfieldvaluetitles = list(
            CustomerFieldValue.objects.all().values_list('field__title',
                                                         flat=True))
        # Iterate over response list
        for data in self.response_has_fields.data:
            # Iterate over customerfieldvaluetitles
            for customerfieldvaluetitle in customerfieldvaluetitles:
                if customerfieldvaluetitle == data['title']:

                    # If customerfieldvalue was found, remove from list
                    customerfieldvaluetitles.remove(customerfieldvaluetitle)
        # No customerfieldvalue shall remain
        self.assertEqual(len(customerfieldvaluetitles), 0)

    def test_add_and_update_customer_field_values(self):
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
            '"customers/tests/test_api.py" - CustomerFieldsListTests: Test adding and updating customer field values')

        # Get customer
        customer = Customer.objects.get(firstname='Dagobert')

        # Adding
        values = [
            "true",                         # Boolean-Checkbox
            "63",                           # Integer-Input
            "3",                            # Integer-Select
            ["2", "3"],                     # Integer-Multiselect
            "1.64",                         # Float-Input
            "12.50",                        # Float-Select
            "2.5",                          # Float-Multiselect
            "Premium Kunde",                # String-Input
            "3 x 2 Stunden in der Woche",   # String-Select
            ["Mittag", "Spät"],             # String-Multiselect
            "2023-07-01"                    # Date-Date
        ]

        id = 11
        for value in values:
            id += 1
            field = FieldMetadata.objects.get(id=id)
            # Add user field
            response_add = self.client.post(
                self.url, {"field": field.id, "value": value}, format='json')

            # Check status code
            self.assertEqual(response_add.status_code, status.HTTP_201_CREATED)

            # Check if customer has id-11 FieldValues now
            self.assertEqual(CustomerFieldValue.objects.filter(
                customer=customer).count(), id-11)

            # Convert value to list, to compare to db entry (which is arrayfield always)
            if isinstance(value, list):
                pass
            else:
                value = [value]

            # Check if correct value was stored in field
            self.assertEqual(CustomerFieldValue.objects.get(
                customer=customer, field=field).value, value)

    def test_add_customer_field_nonexistent_id(self):

        logging.info(
            '"users/tests/test_api.py" - CustomerFieldsListTests: Test adding customer field specifying a nonexistent field')

        # Add user field
        response_add = self.client.post(
            self.url, {"field": FieldMetadata.objects.all().count()+1, "value": 'test'}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_add_customer_field_missing_required_param(self):

        logging.info(
            '"users/tests/test_api.py" - CustomerFieldsListTests: Test adding customer field missing a required parameter (value)')

        # Try adding customer field without value parameter
        response_add = self.client.post(
            self.url, {"field": 1}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Try adding customer field without field parameter
        response_add = self.client.post(
            self.url, {"value": 1}, format='json')

        # Check status code
        self.assertEqual(response_add.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_add_customer_field_with_datatype_mismatch(self):
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
            '"users/tests/test_api.py" - CustomerFieldsListTests: Test adding customer field with wrong datatypes')

        customer = Customer.objects.get(lastname='Duck')

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

        id = 11
        for value in values:
            id += 1

            # Skip the string fields
            if id in [19, 20, 21]:
                pass
            else:
                field = FieldMetadata.objects.get(id=id)
                # Add user field
                response_add = self.client.post(
                    self.url, {"field": field.id, "value": value}, format='json')

                # Check status code
                self.assertEqual(response_add.status_code,
                                 status.HTTP_400_BAD_REQUEST)

                # Check if customer has still 0 FieldValues
                self.assertEqual(CustomerFieldValue.objects.filter(
                    customer=customer).count(), 0)

    def test_add_customer_field_with_wrong_Select_selections(self):
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
            '"users/tests/test_api.py" - CustomerFieldsListTests: Test adding customer field with wrong Select selections')

        customer = Customer.objects.get(lastname='Duck')

        values = [
            "6",                                # Integer-Select
            ["5", "0"],                         # Integer-Multiselect
            "11.50",                            # Float-Select
            ["3.5", "7.2"],                     # Float-Multiselect
            "5x2 Stunden in der Woche",         # String-Select
            "Mitternacht"                       # String-Multiselect
        ]

        id = -1
        field_ids = [14, 15, 17, 18, 20, 21]
        for value in values:
            id += 1
            field = FieldMetadata.objects.get(id=field_ids[id])
            # Add user field
            response_add = self.client.post(
                self.url, {"field": field.id, "value": value}, format='json')

            # Check status code
            self.assertEqual(response_add.status_code,
                             status.HTTP_400_BAD_REQUEST)

            # Check if customer has still 0 FieldValues
            self.assertEqual(CustomerFieldValue.objects.filter(
                customer=customer).count(), 0)


class CustomerFieldsListVisibilityListTest(LoggedInApiTestCase):
    # customer-fields-visibility (GET, POST)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(CustomerFieldsListVisibilityListTest, self).setUp()

        # Get user
        self.user = User.objects.get(username='admin')

        # Get primary key of admin
        self.pk = self.user.pk

        # Specify url
        self.url = reverse(
            'customer-fields-visibility', args=[self.pk])

        self.response = self.client.get(
            self.url, {}, format='json')

    def test_reaching_url(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerFieldsListVisibilityListTest: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_getting_visibility_list(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerFieldsListVisibilityListTest: Test getting visibility preferences')

        # Check if visibility options are matching db_entries
        for field in CustomerCoreFields.get_fields():
            visible = CustomerFieldListVisibility.objects.get(fieldname=field['name'],
                                                              user=self.user).visible

        # Make dict from 'names' and 'values' of visbility fields
        customerfieldlistvisibilities = {}
        # core fields
        for field in CustomerCoreFields.get_fields():
            customerfieldlistvisibilities[field['name']] = CustomerFieldListVisibility.objects.get(fieldname=field['name'],
                                                                                                   user=self.user).visible
        # custom fields
        for field in FieldMetadata.objects.filter(kind=Kind.CUSTOMER):
            customerfieldlistvisibilities[field.name] = CustomerFieldListVisibility.objects.get(fieldname=field.name,
                                                                                                user=self.user).visible

        for data in self.response.data:
            self.assertEqual(
                customerfieldlistvisibilities[data['fieldname']], data['visible'])

        # check correct number of entries
        n_core_fields = len(CustomerCoreFields.get_fields())
        n_custom_fields = len(FieldMetadata.objects.filter(kind=Kind.CUSTOMER))

        self.assertEqual(len(self.response.data),
                         n_core_fields + n_custom_fields)

    def test_changing_visibility_setting(self):

        logging.info(
            '"customers/tests/test_api.py" - CustomerFieldsListVisibilityListTest: Test changing visibility preferences')

        # set visibility of salutation to false
        self.response = self.client.post(
            self.url, {'fieldname': 'salutation', 'visible': False}, format='json')

        self.assertFalse(CustomerFieldListVisibility.objects.get(
            fieldname='salutation',
            user=User.objects.get(username='admin')).visible)
