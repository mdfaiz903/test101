# core/tests/test_models.py

import logging
import datetime
from django.test import Client, TestCase
# local
from core.models import FieldMetadata, FieldType


class FieldMetadataCreationTests(TestCase):

    def setUp(self):
        pass
