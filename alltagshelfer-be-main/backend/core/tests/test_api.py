# core/tests/test_api.py

import logging
import datetime
from django.test import Client, TestCase
from django.urls import include, path, reverse
from rest_framework import status
# local
from core.tests.init_test_setup import LoggedInApiTestCase
from core.models import FieldMetadata, FieldType
from users.models import (User, UserFieldValue,
                          UserFieldListVisibility, build_username)
from customers.models import (Customer, CustomerFieldListVisibility)

# To Test
# fieldmeta-list (GET, POST)
# fieldmeta-detail (GET, PUT, DELETE)
# fieldtypes-list (GET)
# fieldmeta-reorder (PUT)


class FieldMetaListTests(LoggedInApiTestCase):
    # fieldmeta-list (GET)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(FieldMetaListTests, self).setUp()

        # Specify url
        self.url = reverse(
            'fieldmeta-list')

        self.response = self.client.get(
            self.url, {}, format='json')

        self.fields = [
            'id',
            'name',
            'title',
            'kind',
            'default_visible',
            'field_type',
            'placeholder',
            'enums',
            'required',
        ]

    def test_reaching_url(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_list_of_fieldmetadata(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test getting list of all FieldMetadata')

        # Check length of response
        self.assertEqual(len(self.response.data),
                         FieldMetadata.objects.all().count())

        # Check if each FieldMeta contains all fields
        fields = self.fields

        # Check if each fieldmetadata contains all fields
        for fieldmeta in self.response.data:
            for field in fields:
                self.assertTrue(field in fieldmeta)

    def test_get_list_of_fieldmetadata_users(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test getting list of users FieldMetadata')

        self.response = self.client.get(
            self.url, {'kind': 'user'}, format='json')

        # Check length of response
        self.assertEqual(len(self.response.data),
                         FieldMetadata.objects.filter(kind='user').count())

        # Check if each FieldMeta contains all fields
        fields = self.fields

        # Check if each fieldmetadata contains all fields
        for fieldmeta in self.response.data:
            for field in fields:
                self.assertTrue(field in fieldmeta)

    def test_get_list_of_fieldmetadata_customers(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test getting list of customers FieldMetadata')

        self.response = self.client.get(
            self.url, {'kind': 'customer'}, format='json')

        # Check length of response
        self.assertEqual(len(self.response.data),
                         FieldMetadata.objects.filter(kind='customer').count())

        # Check if each FieldMeta contains all fields
        fields = self.fields

        # Check if each fieldmetadata contains all fields
        for fieldmeta in self.response.data:
            for field in fields:
                self.assertTrue(field in fieldmeta)

    def test_adding_fieldmetadata(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test adding FieldMetadata')

        # User

        data = {
            "kind": "user",
            "field_type": {
                "id": 1
            },
            "placeholder": None,
            "default_visible": True,
            "enums": None,
            "title": "Führerschein",
            "required": True
        }

        self.response = self.client.post(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # Check id
        self.assertEqual(
            self.response.data['id'], FieldMetadata.objects.all().count())

        # Check name
        self.assertEqual(self.response.data['name'], 'fuhrerschein')

        # Check required
        self.assertTrue(self.response.data['required'])

        # Check default visible
        self.assertTrue(self.response.data['default_visible'])

        # Check total number of fields
        self.response = self.client.get(
            self.url, {}, format='json')

        # Check length of response
        self.assertEqual(len(self.response.data),
                         FieldMetadata.objects.all().latest('id').id)

        # Check if visibility field was added for all users

        n_user = User.objects.all().count()

        n_fields = UserFieldListVisibility.objects.filter(
            fieldname='fuhrerschein').count()

        self.assertEqual(n_user, n_fields)

        # Customer

        data = {
            "kind": "customer",
            "field_type": {
                "id": 1
            },
            "placeholder": None,
            "default_visible": True,
            "enums": None,
            "title": "Führerschein",
            "required": True
        }

        self.response = self.client.post(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # Check id
        self.assertEqual(
            self.response.data['id'], FieldMetadata.objects.all().count())

        # Check name
        self.assertEqual(self.response.data['name'], 'fuhrerschein')

        # Check required
        self.assertTrue(self.response.data['required'])

        # Check default visible
        self.assertTrue(self.response.data['default_visible'])

        # Check total number of fields
        self.response = self.client.get(
            self.url, {}, format='json')

        # Check length of response
        self.assertEqual(len(self.response.data),
                         FieldMetadata.objects.all().latest('id').id)

        # Check if visibility field was added for all users

        n_user = User.objects.all().count()

        n_fields = CustomerFieldListVisibility.objects.filter(
            fieldname='fuhrerschein').count()

        self.assertEqual(n_user, n_fields)


class FieldMetaDetailTests(LoggedInApiTestCase):
    # fieldmeta-detail (GET, PUT, DELETE)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(FieldMetaDetailTests, self).setUp()

        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='gleitkomma-mehrfachauswahl', kind="user").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Get endpoint
        self.response = self.client.get(
            self.url, {}, format='json')

        self.fields = [
            'id',
            'name',
            'title',
            'kind',
            'default_visible',
            'field_type',
            'placeholder',
            'enums',
            'required',
        ]

    def test_reaching_url(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test reaching URL')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_updating_fieldmetadata_adding_enum_value(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test updating FieldMetadata adding enum value(s)')

        # Add one enum value
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "1.5",
                "2.5",
                "3.5",
                "4"
            ],
            "title": "Gleitkomma Mehrfachauswahl",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entry from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

        # Add more enum values
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "1.5",
                "2.5",
                "3.5",
                "4",
                "7",
                "8.25",
                "9.5",
            ],
            "title": "Gleitkomma Mehrfachauswahl",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entry from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

    def test_updating_fieldmetadata_deleting_unused_enum_value(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test updating FieldMetadata deleting unused enum value(s)')

        # USER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='tatigkeiten', kind="user").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Reinigung" - unused)
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "Einkaufen",
                "Betreuung",
                "Freizeitgestaltung"
            ],
            "title": "Tätigkeiten",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entries from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

        # CUSTIOMER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='bevorzugte tageszeit', kind="customer").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Früh" - used)
        data = {
            "kind": "customer",
            "placeholder": None,
            "enums": [
                "Früh",
                "Mittag"
            ],
            "title": "Bevorzugte Tageszeit",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entries from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

    def test_updating_fieldmetadata_adding_enum_values_and_deleting_unused_enum_value(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test updating FieldMetadata adding new and deleting unused enum value(s)')

        # USER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='tatigkeiten', kind="user").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Reinigung" - unused)
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "Einkaufen",
                "Betreuung",
                "Freizeitgestaltung",
                "Fenster Putzen"
            ],
            "title": "Tätigkeiten",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entries from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

        # CUSTIOMER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='bevorzugte tageszeit', kind="customer").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Früh" - used)
        data = {
            "kind": "customer",
            "placeholder": None,
            "enums": [
                "Früh",
                "Mittag",
                "Mitternachts"
            ],
            "title": "Bevorzugte Tageszeit",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        new_enum_list = data['enums']
        field_enum_list = FieldMetadata.objects.get(pk=self.pk).enums

        # Check if all entries from new_enum_list are stored in the field now
        for entry in field_enum_list:
            for new_enum_entry in new_enum_list:
                if entry == new_enum_entry:
                    new_enum_list.remove(entry)

        self.assertEqual(len(new_enum_list), 0)

    def test_updating_fieldmetadata_deleting_used_enum_value(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test updating FieldMetadata deleting used enum value(s)')

        # USER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='tatigkeiten', kind="user").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Einkaufen" - used)
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "Reinigung",
                "Betreuung",
                "Freizeitgestaltung"
            ],
            "title": "Tätigkeiten",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # All Fields still there
        self.assertEqual(len(FieldMetadata.objects.get(pk=self.pk).enums), 4)

        # CUSTOMER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='bevorzugte tageszeit', kind="customer").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Früh" - used)
        data = {
            "kind": "customer",
            "placeholder": None,
            "enums": [
                "Mittag",
                "Spät",
            ],
            "title": "Bevorzugte Tageszeit",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # All Fields still there
        self.assertEqual(len(FieldMetadata.objects.get(pk=self.pk).enums), 3)

    def test_updating_fieldmetadata_adding_enum_values_and_deleting_used_enum_value(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaDetailTests: Test updating FieldMetadata adding new and deleting used enum value(s)')

        # USER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='tatigkeiten', kind="user").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Einkaufen" - used)
        data = {
            "kind": "user",
            "placeholder": None,
            "enums": [
                "Reinigung",
                "Betreuung",
                "Freizeitgestaltung",
                "Fenster Putzen"
            ],
            "title": "Tätigkeiten",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # All Fields still there
        self.assertEqual(len(FieldMetadata.objects.get(pk=self.pk).enums), 4)

        # New Field is not included
        self.assertFalse(
            "Fenster Putzen" in FieldMetadata.objects.get(pk=self.pk).enums)

        # Deleted Field is still included
        self.assertTrue(
            "Einkaufen" in FieldMetadata.objects.get(pk=self.pk).enums)

        # Check if enum list is returned (to display it in the form)
        enum_response = self.response.data["enums_complete"]

        for d in enum_response:
            self.assertTrue(d in [
                            "Reinigung", "Betreuung", "Freizeitgestaltung", "Fenster Putzen", "Einkaufen"])

        # CUSTOMER FIELD
        # Get primary key of field
        self.pk = FieldMetadata.objects.get(
            name='bevorzugte tageszeit', kind="customer").pk

        # Specify url ()
        self.url = reverse(
            'fieldmeta-detail', args=[self.pk])

        # Delete one enum value ("Früh" - used)
        data = {
            "kind": "customer",
            "placeholder": None,
            "enums": [
                "Mittag",
                "Spät",
                "Mitternacht"
            ],
            "title": "Bevorzugte Tageszeit",
            "required": False,
            "default_visible": False
        }

        self.response = self.client.put(
            self.url, data, format='json')

        # Check status code
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # All Fields still there
        self.assertEqual(len(FieldMetadata.objects.get(pk=self.pk).enums), 3)

        # New Field is not included
        self.assertFalse(
            "Mitternacht" in FieldMetadata.objects.get(pk=self.pk).enums)

        # Deleted Field is still included
        self.assertTrue(
            "Früh" in FieldMetadata.objects.get(pk=self.pk).enums)

        # Check if enum list is returned (to display it in the form)
        enum_response = self.response.data["enums_complete"]

        for d in enum_response:
            self.assertTrue(d in [
                            "Früh", "Mittag", "Spät", "Mitternacht"])


class FieldMetaReorderTests(LoggedInApiTestCase):
    # fieldmeta-list (GET)

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Perform login
        super(FieldMetaReorderTests, self).setUp()

        # Specify url
        self.url = reverse(
            'fieldmeta-reorder')

    def test_reordering_customfields_correctly(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test reordering of FieldMetadata')

        # USER FIELDS

        # change position of id=10 and id=11
        self.user_fields_reorder = [{'kind': 'user',
                                     'order': [
                                         {
                                             "id": 1,
                                             "position": 0
                                         },
                                         {
                                             "id": 2,
                                             "position": 1
                                         },
                                         {
                                             "id": 3,
                                             "position": 2
                                         },
                                         {
                                             "id": 5,
                                             "position": 3
                                         },
                                         {
                                             "id": 4,
                                             "position": 4
                                         },
                                         {
                                             "id": 6,
                                             "position": 5
                                         },
                                         {
                                             "id": 7,
                                             "position": 6
                                         },
                                         {
                                             "id": 8,
                                             "position": 7
                                         },
                                         {
                                             "id": 9,
                                             "position": 8
                                         },
                                         {
                                             "id": 11,
                                             "position": 9
                                         },
                                         {
                                             "id": 10,
                                             "position": 10
                                         }
                                     ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check positions
        for field in FieldMetadata.objects.filter(kind="user"):
            if field.id == 11:
                self.assertEqual(field.position, 9)
            elif field.id == 10:
                self.assertEqual(field.position, 10)

        # CUSTOMER FIELDS

        # change position of id=14 and id=15
        self.customer_fields_reorder = [{'kind': 'customer',
                                        'order': [
                                            {
                                                "id": 12,
                                                "position": 0
                                            },
                                            {
                                                "id": 13,
                                                "position": 1
                                            },
                                            {
                                                "id": 15,
                                                "position": 2
                                            },
                                            {
                                                "id": 14,
                                                "position": 3
                                            },
                                            {
                                                "id": 16,
                                                "position": 4
                                            },
                                            {
                                                "id": 17,
                                                "position": 5
                                            },
                                            {
                                                "id": 18,
                                                "position": 6
                                            },
                                            {
                                                "id": 19,
                                                "position": 7
                                            },
                                            {
                                                "id": 20,
                                                "position": 8
                                            },
                                            {
                                                "id": 21,
                                                "position": 9
                                            },
                                            {
                                                "id": 22,
                                                "position": 10
                                            }
                                        ]}]

        # put
        response = self.client.put(
            self.url, self.customer_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check positions
        for field in FieldMetadata.objects.filter(kind="customer"):
            if field.id == 15:
                self.assertEqual(field.position, 2)
            elif field.id == 14:
                self.assertEqual(field.position, 3)

    def test_reordering_customfields_with_missing_fields(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test reordering of FieldMetadata with missing Fields')

        # USER FIELDS

        # id=1 and id=2 missing
        self.user_fields_reorder = [{'kind': 'user',
                                    'order': [
                                        {
                                            "id": 3,
                                            "position": 2
                                        },
                                        {
                                            "id": 5,
                                            "position": 3
                                        },
                                        {
                                            "id": 4,
                                            "position": 4
                                        },
                                        {
                                            "id": 6,
                                            "position": 5
                                        },
                                        {
                                            "id": 7,
                                            "position": 6
                                        },
                                        {
                                            "id": 8,
                                            "position": 7
                                        },
                                        {
                                            "id": 9,
                                            "position": 8
                                        },
                                        {
                                            "id": 11,
                                            "position": 9
                                        },
                                        {
                                            "id": 10,
                                            "position": 10
                                        }
                                    ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="user"):
            if field.id == 1:
                self.assertEqual(field.position, 0)
            elif field.id == 2:
                self.assertEqual(field.position, 1)
            elif field.id == 3:
                self.assertEqual(field.position, 2)
            elif field.id == 4:
                self.assertEqual(field.position, 3)
            elif field.id == 5:
                self.assertEqual(field.position, 4)
            elif field.id == 6:
                self.assertEqual(field.position, 5)
            elif field.id == 7:
                self.assertEqual(field.position, 6)
            elif field.id == 8:
                self.assertEqual(field.position, 7)
            elif field.id == 9:
                self.assertEqual(field.position, 8)
            elif field.id == 10:
                self.assertEqual(field.position, 9)
            elif field.id == 11:
                self.assertEqual(field.position, 10)

        # CUSTOMER FIELDS

        # id=12 and id=13 missing
        self.customer_fields_reorder = [{'kind': 'customer',
                                        'order': [
                                            {
                                                "id": 15,
                                                "position": 2
                                            },
                                            {
                                                "id": 14,
                                                "position": 3
                                            },
                                            {
                                                "id": 16,
                                                "position": 4
                                            },
                                            {
                                                "id": 17,
                                                "position": 5
                                            },
                                            {
                                                "id": 18,
                                                "position": 6
                                            },
                                            {
                                                "id": 19,
                                                "position": 7
                                            },
                                            {
                                                "id": 20,
                                                "position": 8
                                            },
                                            {
                                                "id": 21,
                                                "position": 9
                                            },
                                            {
                                                "id": 22,
                                                "position": 10
                                            }
                                        ]}]

        # put
        response = self.client.put(
            self.url, self.customer_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="customer"):
            if field.id == 12:
                self.assertEqual(field.position, 0)
            elif field.id == 13:
                self.assertEqual(field.position, 1)
            elif field.id == 14:
                self.assertEqual(field.position, 2)
            elif field.id == 15:
                self.assertEqual(field.position, 3)
            elif field.id == 16:
                self.assertEqual(field.position, 4)
            elif field.id == 17:
                self.assertEqual(field.position, 5)
            elif field.id == 18:
                self.assertEqual(field.position, 6)
            elif field.id == 19:
                self.assertEqual(field.position, 7)
            elif field.id == 20:
                self.assertEqual(field.position, 8)
            elif field.id == 21:
                self.assertEqual(field.position, 9)
            elif field.id == 22:
                self.assertEqual(field.position, 10)

    def test_reordering_customfields_with_doubled_positions(self):

        logging.info(
            '"core/tests/test_api.py" - FieldMetaListTests: Test reordering of FieldMetadata with doubled and inconsistent positions (with gaps)')

        # USER FIELDS

        # id=10 and id=11 have same position
        self.user_fields_reorder = [{'kind': 'user',
                                     'order': [
                                         {
                                             "id": 1,
                                             "position": 0
                                         },
                                         {
                                             "id": 2,
                                             "position": 1
                                         },
                                         {
                                             "id": 3,
                                             "position": 2
                                         },
                                         {
                                             "id": 5,
                                             "position": 3
                                         },
                                         {
                                             "id": 4,
                                             "position": 4
                                         },
                                         {
                                             "id": 6,
                                             "position": 5
                                         },
                                         {
                                             "id": 7,
                                             "position": 6
                                         },
                                         {
                                             "id": 8,
                                             "position": 7
                                         },
                                         {
                                             "id": 9,
                                             "position": 8
                                         },
                                         {
                                             "id": 11,
                                             "position": 9
                                         },
                                         {
                                             "id": 10,
                                             "position": 9
                                         }
                                     ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="user"):
            if field.id == 1:
                self.assertEqual(field.position, 0)
            elif field.id == 2:
                self.assertEqual(field.position, 1)
            elif field.id == 3:
                self.assertEqual(field.position, 2)
            elif field.id == 4:
                self.assertEqual(field.position, 3)
            elif field.id == 5:
                self.assertEqual(field.position, 4)
            elif field.id == 6:
                self.assertEqual(field.position, 5)
            elif field.id == 7:
                self.assertEqual(field.position, 6)
            elif field.id == 8:
                self.assertEqual(field.position, 7)
            elif field.id == 9:
                self.assertEqual(field.position, 8)
            elif field.id == 10:
                self.assertEqual(field.position, 9)
            elif field.id == 11:
                self.assertEqual(field.position, 10)

        # position 10 is skipped
        self.user_fields_reorder = [{'kind': 'user',
                                     'order': [
                                         {
                                             "id": 1,
                                             "position": 0
                                         },
                                         {
                                             "id": 2,
                                             "position": 1
                                         },
                                         {
                                             "id": 3,
                                             "position": 2
                                         },
                                         {
                                             "id": 5,
                                             "position": 3
                                         },
                                         {
                                             "id": 4,
                                             "position": 4
                                         },
                                         {
                                             "id": 6,
                                             "position": 5
                                         },
                                         {
                                             "id": 7,
                                             "position": 6
                                         },
                                         {
                                             "id": 8,
                                             "position": 7
                                         },
                                         {
                                             "id": 9,
                                             "position": 8
                                         },
                                         {
                                             "id": 11,
                                             "position": 9
                                         },
                                         {
                                             "id": 10,
                                             "position": 11
                                         }
                                     ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="user"):
            if field.id == 1:
                self.assertEqual(field.position, 0)
            elif field.id == 2:
                self.assertEqual(field.position, 1)
            elif field.id == 3:
                self.assertEqual(field.position, 2)
            elif field.id == 4:
                self.assertEqual(field.position, 3)
            elif field.id == 5:
                self.assertEqual(field.position, 4)
            elif field.id == 6:
                self.assertEqual(field.position, 5)
            elif field.id == 7:
                self.assertEqual(field.position, 6)
            elif field.id == 8:
                self.assertEqual(field.position, 7)
            elif field.id == 9:
                self.assertEqual(field.position, 8)
            elif field.id == 10:
                self.assertEqual(field.position, 9)
            elif field.id == 11:
                self.assertEqual(field.position, 10)

        # CUSTOMER FIELDS

        # id=14 and id=15 have same position
        self.customer_fields_reorder = [{'kind': 'customer',
                                        'order': [
                                            {
                                                "id": 12,
                                                "position": 0
                                            },
                                            {
                                                "id": 13,
                                                "position": 1
                                            },
                                            {
                                                "id": 14,
                                                "position": 2
                                            },
                                            {
                                                "id": 15,
                                                "position": 2
                                            },
                                            {
                                                "id": 16,
                                                "position": 3
                                            },
                                            {
                                                "id": 17,
                                                "position": 4
                                            },
                                            {
                                                "id": 18,
                                                "position": 5
                                            },
                                            {
                                                "id": 19,
                                                "position": 6
                                            },
                                            {
                                                "id": 20,
                                                "position": 7
                                            },
                                            {
                                                "id": 21,
                                                "position": 8
                                            },
                                            {
                                                "id": 22,
                                                "position": 9
                                            }
                                        ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="customer"):
            if field.id == 12:
                self.assertEqual(field.position, 0)
            elif field.id == 13:
                self.assertEqual(field.position, 1)
            elif field.id == 14:
                self.assertEqual(field.position, 2)
            elif field.id == 15:
                self.assertEqual(field.position, 3)
            elif field.id == 16:
                self.assertEqual(field.position, 4)
            elif field.id == 17:
                self.assertEqual(field.position, 5)
            elif field.id == 18:
                self.assertEqual(field.position, 6)
            elif field.id == 19:
                self.assertEqual(field.position, 7)
            elif field.id == 20:
                self.assertEqual(field.position, 8)
            elif field.id == 21:
                self.assertEqual(field.position, 9)
            elif field.id == 22:
                self.assertEqual(field.position, 10)

        # position 3 is skipped
        self.customer_fields_reorder = [{'kind': 'customer',
                                        'order': [
                                            {
                                                "id": 12,
                                                "position": 0
                                            },
                                            {
                                                "id": 13,
                                                "position": 1
                                            },
                                            {
                                                "id": 14,
                                                "position": 2
                                            },
                                            {
                                                "id": 15,
                                                "position": 4
                                            },
                                            {
                                                "id": 16,
                                                "position": 5
                                            },
                                            {
                                                "id": 17,
                                                "position": 6
                                            },
                                            {
                                                "id": 18,
                                                "position": 7
                                            },
                                            {
                                                "id": 19,
                                                "position": 8
                                            },
                                            {
                                                "id": 20,
                                                "position": 9
                                            },
                                            {
                                                "id": 21,
                                                "position": 10
                                            },
                                            {
                                                "id": 22,
                                                "position": 11
                                            }
                                        ]}]

        # put
        response = self.client.put(
            self.url, self.user_fields_reorder, format='json')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check positions (still same?)
        for field in FieldMetadata.objects.filter(kind="customer"):
            if field.id == 12:
                self.assertEqual(field.position, 0)
            elif field.id == 13:
                self.assertEqual(field.position, 1)
            elif field.id == 14:
                self.assertEqual(field.position, 2)
            elif field.id == 15:
                self.assertEqual(field.position, 3)
            elif field.id == 16:
                self.assertEqual(field.position, 4)
            elif field.id == 17:
                self.assertEqual(field.position, 5)
            elif field.id == 18:
                self.assertEqual(field.position, 6)
            elif field.id == 19:
                self.assertEqual(field.position, 7)
            elif field.id == 20:
                self.assertEqual(field.position, 8)
            elif field.id == 21:
                self.assertEqual(field.position, 9)
            elif field.id == 22:
                self.assertEqual(field.position, 10)
