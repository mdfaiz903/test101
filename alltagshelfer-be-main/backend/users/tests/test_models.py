# users/tests/test_models.py

import logging
import datetime
from django.test import Client, TestCase
# local
from core.models import FieldMetadata
from users.models import User, UserFieldValue, build_username, UserRoles
from .constants import TEST_CAREGIVER, TEST_SUPERVISOR, TEST_CEO, TEST_ADMIN
from .constants import (TEST_CAREGIVER_OUTPUTS,
                        TEST_SUPERVISOR_OUTPUTS, TEST_CEO_OUTPUTS,
                        TEST_ADMIN_OUTPUTS)


class FixturesTestCase(TestCase):
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


class UsernameCreationTests(FixturesTestCase):
    """
    test building usernames
    """

    def setUp(self):
        self.firstname = "Matthäus"
        self.lastname = "Gökdeniz"
        self.username = "matthaeusgoekdeniz"

    def test_building_usernames(self):
        logging.info('UsernameCreationTests: Test building usernames')
        # Buid username
        username = build_username(
            firstname=self.firstname, lastname=self.lastname)

        # Check if username was built correctly
        self.assertEqual(username, self.username)

        # Create User with given username
        user1 = User.objects.create_user(
            username=username, password="testpassword1234")

        # Build username again
        username = build_username(
            firstname=self.firstname, lastname=self.lastname)

        # Check if username was built correctly (_1)
        self.assertEqual(username, self.username + '_1')

        # Create another User with given username
        User.objects.create_user(
            username=username, password="testpassword1234")

        # Delete first user
        user1.delete()

        # Build username again
        username = build_username(
            firstname=self.firstname, lastname=self.lastname)

        # Check if username was built correctly (_2)
        self.assertEqual(username, self.username + '_2')


class CreateUserTests(FixturesTestCase):
    """
    test creating users
    """

    def setUp(self):

        # Create Caregiver
        username = build_username(
            firstname=TEST_CAREGIVER['firstname'],
            lastname=TEST_CAREGIVER['lastname'])
        User.objects.create_user(username=username, **TEST_CAREGIVER)

        # Create Supervisor
        username = build_username(
            firstname=TEST_SUPERVISOR['firstname'],
            lastname=TEST_SUPERVISOR['lastname'])
        User.objects.create_user(username=username, **TEST_SUPERVISOR)

        # Create CEO
        username = build_username(
            firstname=TEST_CEO['firstname'],
            lastname=TEST_CEO['lastname'])
        User.objects.create_user(username=username, **TEST_CEO)

        # Create ADMIN
        username = build_username(
            firstname=TEST_ADMIN['firstname'],
            lastname=TEST_ADMIN['lastname'])
        User.objects.create_user(username=username, **TEST_ADMIN)

    def test_string_representation(self):
        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test string representation')
        self.assertEqual(str(User.objects.get(
            lastname=TEST_CAREGIVER['lastname'])),
            TEST_CAREGIVER_OUTPUTS['username'])

    def test_user_creation_dates(self):
        """
        test if creation_dates were set correctly
        """
        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test creation dates')
        # Caregiver
        self.assertEqual(User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).date_joined.date(),
            datetime.date.today())
        # Supervisor
        self.assertEqual(User.objects.get(
            lastname=TEST_SUPERVISOR['lastname']).date_joined.date(),
            datetime.date.today())
        # CEO
        self.assertEqual(User.objects.get(
            lastname=TEST_CEO['lastname']).date_joined.date(),
            datetime.date.today())
        # Admin
        self.assertEqual(User.objects.get(
            lastname=TEST_ADMIN['lastname']).date_joined.date(),
            datetime.date.today())

    def test_authentication(self):
        """
        test if passwords were set correctly
        """

        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test authentication')
        # Setup client for authentication# Setup client for authentication
        c = Client()

        # Test "Alltagshelfer" authentication
        self.assertTrue(c.login(username=TEST_CAREGIVER_OUTPUTS['username'],
                        password=TEST_CAREGIVER['password']))
        c.logout()

        # Test "Supervisor" authentication
        self.assertTrue(c.login(username=TEST_SUPERVISOR_OUTPUTS['username'],
                        password=TEST_SUPERVISOR['password']))
        c.logout()

        # Test "CEO" authentication
        self.assertTrue(c.login(username=TEST_CEO_OUTPUTS['username'],
                        password=TEST_CEO['password']))
        c.logout()

        # Test "Admin" authentication
        self.assertTrue(c.login(username=TEST_ADMIN_OUTPUTS['username'],
                        password=TEST_ADMIN['password']))
        c.logout()

    def test_user_roles(self):
        """
        test if user roles were set correctly
        """

        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test user roles')

        # Caregiver
        self.assertEqual(User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).role, UserRoles.CAREGIVER)
        # Supervisor
        self.assertEqual(User.objects.get(
            lastname=TEST_SUPERVISOR['lastname']).role, UserRoles.SUPERVISOR)
        # CEO
        self.assertEqual(User.objects.get(
            lastname=TEST_CEO['lastname']).role, UserRoles.CEO)
        # Admin
        self.assertEqual(User.objects.get(
            lastname=TEST_ADMIN['lastname']).role, UserRoles.ADMIN)

        # Test is Admin is superuser and staff
        self.assertTrue(User.objects.get(
            lastname=TEST_ADMIN['lastname']).is_staff)
        self.assertTrue(User.objects.get(
            lastname=TEST_ADMIN['lastname']).is_superuser)

    def test_creating_user_without_password(self):
        """
        test creating user without password
        """

        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test creating user without password')

        # "Normal" users
        with self.assertRaisesRegex(ValueError, 'Please provide a password'):
            User.objects.create_user(
                username=TEST_CAREGIVER_OUTPUTS['username'])

        # "Admins"
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                username=TEST_ADMIN_OUTPUTS['username'])

    def test_creating_superuser(self):

        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test creating superuser')

        self.assertEqual(User.objects.create_superuser(
            username=TEST_ADMIN_OUTPUTS['username']+'_1',
            password=TEST_ADMIN['password']).date_joined.date(),
            datetime.date.today())

        # Assure that duplicate role definition doesn't lead to an error
        self.assertEqual(User.objects.create_superuser(
            username=TEST_ADMIN_OUTPUTS['username']+'_2',
            password=TEST_ADMIN['password'], role='admin').date_joined.date(),
            datetime.date.today())

    def test_creating_user_with_duplicate_username(self):

        logging.info(
            '"users/tests/test_models.py" - CreateUserTests: Test creating user with duplicate username')

        # "Normal" users
        with self.assertRaisesRegex(ValueError, 'Username already existing'):
            User.objects.create_user(
                username=TEST_CAREGIVER_OUTPUTS['username'],
                password=TEST_CAREGIVER['password'])

        # "Admins"
        with self.assertRaisesRegex(ValueError, 'Username already existing'):
            User.objects.create_superuser(
                username=TEST_ADMIN_OUTPUTS['username'],
                password=TEST_ADMIN['password'])


class UpdateUserTests(FixturesTestCase):
    """
    test updating users
    """

    def setUp(self):
        # Create Caregiver
        username = build_username(
            firstname=TEST_CAREGIVER['firstname'],
            lastname=TEST_CAREGIVER['lastname'])
        user = User.objects.create_user(username=username, **TEST_CAREGIVER)

        # Update field
        user.street = 'Musterstraße'

        # Update role
        user.role = 'CEO'
        user.save()

    def test_updating_fields(self):

        logging.info(
            '"users/tests/test_models.py" - UpdateUserTests: Test updating user fields')

        self.assertEqual(User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).street, 'Musterstraße')

    def test_updating_role(self):

        logging.info(
            '"users/tests/test_models.py" - UpdateUserTests: Test updating user role')

        self.assertEqual(User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).role, UserRoles.CEO)


class DeleteUserTests(FixturesTestCase):
    """
    test deleting users
    """

    def setUp(self):
        # Create Caregiver
        username = build_username(
            firstname=TEST_CAREGIVER['firstname'],
            lastname=TEST_CAREGIVER['lastname'])
        User.objects.create_user(username=username, **TEST_CAREGIVER)

    def test_delete_user(self):

        logging.info(
            '"users/tests/test_models.py" - DeleteUserTests: Test deleting user')

        User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).delete()

        # Check if deleted-"flag" was set
        self.assertTrue(User.objects.get(
            lastname=TEST_CAREGIVER['lastname']).deleted)

        # Check if user is not listed anymore when filtering deleted
        self.assertFalse(User.objects.filter(
            lastname=TEST_CAREGIVER['lastname'], deleted=False).exists())


class UserFieldValuesTests(FixturesTestCase):
    """
    test user field values
    """

    def setUp(self):
        # Get Field "Vertragsart"
        self.field = FieldMetadata.objects.get(title="Vertragsart")
        # Specify user
        self.user = User.objects.get(pk='735dc5b8-b3d2-4f64-a4c1-9f34bada291a')

    def test_string_representation(self):

        logging.info(
            '"users/tests/test_models.py" - UserFieldValuesTests: Test string representation')

        # Get field with title "Vertragsart"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=self.field)
        # Check if field "Vertragsart" was added to user
        self.assertEqual(str(userfieldval), 'Vertragsart')

        # Check if correct value was set
        self.assertEqual(userfieldval.value, ['Teilzeit'])

    def test_listing_fields_per_user(self):

        logging.info(
            '"users/tests/test_models.py" - UserFieldValuesTests: Test listing fields')

        # Get all custom fields of user
        userfieldvals = UserFieldValue.objects.filter(user=self.user)

        # Check number of UserFields - should be 4 fields
        self.assertEqual(userfieldvals.count(), 4)

        # Get field with title "Vertragsart"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=self.field)

        # Check if correct value was set
        self.assertEqual(userfieldval.value, ['Teilzeit'])

    def test_adding_fields(self):

        logging.info(
            '"users/tests/test_models.py" - UserFieldValuesTests: Test adding fields')

        # New Field "Berufsausbildung"
        field = FieldMetadata.objects.get(title="Berufsausbildung")

        # Create new field
        UserFieldValue.objects.create(user=self.user,
                                      field=field,
                                      value=['true'])

        # Get all custom fields of user
        userfieldvals = UserFieldValue.objects.filter(user=self.user)

        # Check number of UserFields - should be 5 fields now
        self.assertEqual(userfieldvals.count(), 5)

        # Get field with title "Berufsausbildung"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=field)

        # Check number of UserFields - should be 3 fields
        self.assertEqual(userfieldval.value, ['true'])

    def test_updating_field_values(self):

        logging.info(
            '"users/tests/test_models.py" - UserFieldValuesTests: Test updating fields')

        # Get field with title "Vertragsart"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=self.field)

        # Set new value
        userfieldval.value = ['Freiberufler']

        # Save new userfieldval
        userfieldval.save()

        # Get field with title "Vertragsart"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=self.field)

        # Check if correct value was set
        self.assertEqual(userfieldval.value, ['Freiberufler'])

    def test_deleting_field_values(self):

        logging.info(
            '"users/tests/test_models.py" - UserFieldValuesTests: Test deleting fields')

        # userfieldval field with title "Vertragsart"
        userfieldval = UserFieldValue.objects.get(user=self.user,
                                                  field=self.field)

        # Delete UserFieldValue
        userfieldval.delete()

        # Get all user field values
        userfieldvals = UserFieldValue.objects.filter(user=self.user)

        # Check number of UserFields - should be 3 fields now
        self.assertTrue(userfieldvals.count() == 3)
