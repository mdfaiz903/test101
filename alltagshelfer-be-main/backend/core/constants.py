# core/constants.py

from dataclasses import dataclass


@dataclass
class Weekdays:
    MONDAY = 'Montag'
    TUESDAY = 'Dienstag'
    WEDNESDAY = 'Mittwoch'
    THURSDAY = 'Donnerstag'
    FRIDAY = 'Freitag'
    SATURDAY = 'Samstag'
    SUNDAY = 'Sonntag'


@dataclass
class Frequencies:
    DAIlY = 'Täglich'
    WEEKLY = 'Wöchentlich'
    BIWEEKLY = '2-Wöchentlich'
    MONTHLY = 'Monatlich'
    BIMONTHLY = '2-Monatlich'
    QUATERLY = 'Vierteljährlich'
    HALFYEARLY = 'Halbjährlich'
    YEARLY = 'Jährlich'


@dataclass
class DataTypes:
    BOOLEAN = "boolean"
    INT = "integer"
    FLOAT = "float"
    STRING = "string"
    DATE = "date"


@dataclass
class InputTypes:
    MULTISELECT = "multiselect"
    SELECT = "select"
    CHECKBOX = "checkbox"
    INPUT = "input"
    DATE = "date"


@dataclass
class Kind:
    USER = 'user'
    CUSTOMER = 'customer'


@dataclass
class Salutations:
    MR = 'Herr'
    MS = 'Frau'
    DIVERS = 'Divers'

    @classmethod
    def get_salutations(cls):
        return [Salutations.MR,
                Salutations.MS,
                Salutations.DIVERS]


@dataclass
class UserRoles:
    CAREGIVER = "CAREGIVER"
    SUPERVISOR = "SUPERVISOR"
    CEO = "CEO"
    ADMIN = "ADMIN"

    @classmethod
    def get_roles(cls):
        return [UserRoles.CAREGIVER,
                UserRoles.SUPERVISOR,
                UserRoles.CEO,
                UserRoles.ADMIN]
