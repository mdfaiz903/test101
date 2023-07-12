# customers/constants.py

import logging
from dataclasses import dataclass
from core.constants import DataTypes, InputTypes, Salutations


@dataclass
class CustomerCoreFields:
    """
    defines field types supported by application & their attributes
    """

    SALUTATION = {"name": "salutation",
                  "title": "Anrede",
                  "id": "0",
                  "kind": "customer",
                  "position": 0,
                  "enums": Salutations.get_salutations(),
                  "placeholder": None,
                  "data_type": DataTypes.STRING,
                  "input_type": InputTypes.SELECT,
                  "visible": True,
                  "required": True}

    LASTNAME = {"name": "lastname",
                "title": "Nachname",
                "id": "0",
                "kind": "customer",
                "position": 1,
                "enums": [],
                "placeholder": None,
                "data_type": DataTypes.STRING,
                "input_type": InputTypes.INPUT,
                "visible": True,
                "required": True}

    FIRSTNAME = {"name": "firstname",
                 "title": "Vorname",
                 "id": "0",
                 "kind": "customer",
                 "position": 2,
                 "enums": [],
                 "placeholder": None,
                 "data_type": DataTypes.STRING,
                 "input_type": InputTypes.INPUT,
                 "visible": True,
                 "required": True}

    STREET = {"name": "street",
              "title": "Straße",
              "id": "0",
              "kind": "customer",
              "position": 3,
              "enums": [],
              "placeholder": None,
              "data_type": DataTypes.STRING,
              "input_type": InputTypes.INPUT,
              "visible": False,
              "required": False}

    HOUSE_NUMBER = {"name": "house_number",
                    "title": "Hausnummer",
                    "id": "0",
                    "kind": "customer",
                    "position": 4,
                    "enums": [],
                    "placeholder": None,
                    "data_type": DataTypes.STRING,
                    "input_type": InputTypes.INPUT,
                    "visible": False,
                    "required": False}

    CITY = {"name": "city",
            "title": "Ort",
            "id": "0",
            "kind": "customer",
            "position": 5,
            "enums": [],
            "placeholder": None,
            "data_type": DataTypes.STRING,
            "input_type": InputTypes.INPUT,
            "visible": True,
            "required": False}

    ZIP = {"name": "zip",
           "title": "PLZ",
           "id": "0",
           "kind": "customer",
           "position": 6,
           "enums": [],
           "placeholder": None,
           "data_type": DataTypes.STRING,
           "input_type": InputTypes.INPUT,
           "visible": False,
           "required": False}

    ADDRESS_ADDITION = {"name": "address_addition",
                        "title": "Adresszusatz",
                        "id": "0",
                        "kind": "customer",
                        "position": 7,
                        "enums": [],
                        "placeholder": None,
                        "data_type": DataTypes.STRING,
                        "input_type": InputTypes.INPUT,
                        "visible": False,
                        "required": False}

    PHONE_MOBILE = {"name": "phone_mobile",
                    "title": "Mobilnummer",
                    "id": "0",
                    "kind": "customer",
                    "position": 8,
                    "enums": [],
                    "placeholder": None,
                    "data_type": DataTypes.STRING,
                    "input_type": InputTypes.INPUT,
                    "visible": False,
                    "required": False}

    PHONE_HOUSE = {"name": "phone_house",
                   "title": "Telefonnummer",
                   "id": "0",
                   "kind": "customer",
                   "position": 9,
                   "enums": [],
                   "placeholder": None,
                   "data_type": DataTypes.STRING,
                   "input_type": InputTypes.INPUT,
                   "visible": False,
                   "required": False}

    BIRTHDAY = {"name": "birthday",
                "title": "Geburtsdatum",
                "id": "0",
                "kind": "customer",
                "position": 10,
                "enums": [],
                "placeholder": None,
                "data_type": DataTypes.DATE,
                "input_type": InputTypes.DATE,
                "visible": False,
                "required": False}

    EMAIL = {"name": "email",
             "title": "E-Mail",
             "id": "0",
             "kind": "customer",
             "position": 11,
             "enums": [],
             "placeholder": None,
             "data_type": DataTypes.STRING,
             "input_type": InputTypes.INPUT,
             "visible": False,
             "required": False}

    COMMENTS = {"name": "comments",
                "title": "Kommentar",
                "id": "0",
                "kind": "customer",
                "position": 12,
                "enums": [],
                "placeholder": None,
                "data_type": DataTypes.STRING,
                "input_type": InputTypes.INPUT,
                "visible": False,
                "required": False}

    CREATED_AT = {"name": "created_at",
                  "title": "Erstellt am",
                  "id": "0",
                  "kind": "customer",
                  "position": 13,
                  "enums": [],
                  "placeholder": None,
                  "data_type": DataTypes.DATE,
                  "input_type": InputTypes.DATE,
                  "visible": False,
                  "required": False}

    MODIFIED_AT = {"name": "modified_at",
                   "title": "Bearbeitet am",
                   "id": "0",
                   "kind": "customer",
                   "position": 14,
                   "enums": [],
                   "placeholder": None,
                   "data_type": DataTypes.DATE,
                   "input_type": InputTypes.DATE,
                   "visible": False,
                   "required": False}

    AUTHOR = {"name": "author",
              "title": "Erstellt von",
              "id": "0",
              "kind": "customer",
              "position": 15,
              "enums": [],
              "placeholder": None,
              "data_type": DataTypes.STRING,
              "input_type": InputTypes.INPUT,
              "visible": False,
              "required": False}

    @classmethod
    def get_fieldinfo_by_name(cls, name: str):
        """
        Returns the data_type and input_type of a given id.
        """
        # Iterate over allowed fields
        for value in cls.__dict__.values():
            try:
                # If 'name' matches name-input
                if value['name'] == name:
                    title = value['title']
                    position = value['position']
                    enums = value['enums']
                    placeholder = value['placeholder']
                    data_type = value['data_type']
                    input_type = value['input_type']
                    required = value['required']
                    visible = value['visible']
                    exists = True
                    break
            except (TypeError, KeyError):
                title = ""
                position = 99
                enums = []
                data_type = ""
                input_type = ""
                placeholder = ""
                required = ""
                visible = ""
                exists = False

        fieldinfo: dict[str, float] = {
            "title": title,
            "position": position,
            "enums": enums,
            "placeholder": placeholder,
            "data_type": data_type,
            "input_type": input_type,
            "visible": visible,
            "required": required,
            "exists": exists}

        return fieldinfo

    @classmethod
    def get_fields(cls):
        """
        Returns all fields
        """

        fields = []

        # Iterate over allowed fields
        for value in cls.__dict__.values():
            try:
                if value['name']:
                    # Add field_type to value
                    value['field_type'] = {
                        'id': '0',
                        'input_type': value['input_type'],
                        'data_type': value['data_type']
                    }
                    fields.append(value)
            except (TypeError, KeyError):
                pass

        return fields
