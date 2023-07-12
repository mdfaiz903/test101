# GET USER LIST

Endpoint: <code>/api/users/</code>  (GET)

## REQUEST HEADER
|Key|Value|
|-|-|
|Content-Type|application/vnd.api+json|
|Authorization|Bearer \<token>|

## EXAMPLES

### Get all users
```yaml
-Server response (200 OK)-
{
    "data": [
        {
            "type": "User",
            "id": "1a12c49d-8192-4e24-9e97-751c08fbde14",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": null,
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_6",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": null,
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": null,
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": null,
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": null,
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": null,
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": null,
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": null,
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": null,
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": null,
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": null,
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 160.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": null,
                "lastname": "Müller",
                "firstname": "Martin",
                "street": null,
                "house_number": null,
                "city": null,
                "zip": null,
                "address_addition": null,
                "phone_mobile": null,
                "phone_house": null,
                "birthday": null,
                "email": null,
                "comments": null,
                "role": "CAREGIVER",
                "username": "martinmueller_6",
                "monthly_working_hours": 160.0
            }
        },
        {
            "type": "User",
            "id": "07c42889-0b2a-4f38-b335-ac78ea424536",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": null,
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_5",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": null,
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": null,
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": null,
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": null,
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": null,
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": null,
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": null,
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": null,
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": null,
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": null,
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "ADMIN",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 160.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": null,
                "lastname": "Müller",
                "firstname": "Martin",
                "street": null,
                "house_number": null,
                "city": null,
                "zip": null,
                "address_addition": null,
                "phone_mobile": null,
                "phone_house": null,
                "birthday": null,
                "email": null,
                "comments": null,
                "role": "ADMIN",
                "username": "martinmueller_5",
                "monthly_working_hours": 160.0
            }
        },
        {
            "type": "User",
            "id": "51723a61-373c-4d1e-9d08-f98dde61439d",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": "Herr",
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_4",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": "Mellinghoferstr.",
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": "16a",
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": "Oberhausen",
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": "46047",
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": "Seiteneingang",
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": "0151 123456789",
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": "0208 123456789",
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": "1992-11-10",
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "martin.mueller@testmail.com",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "Kommentar",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 80.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": "Herr",
                "lastname": "Müller",
                "firstname": "Martin",
                "street": "Mellinghoferstr.",
                "house_number": "16a",
                "city": "Oberhausen",
                "zip": "46047",
                "address_addition": "Seiteneingang",
                "phone_mobile": "0151 123456789",
                "phone_house": "0208 123456789",
                "birthday": "1992-11-10",
                "email": "martin.mueller@testmail.com",
                "comments": "Kommentar",
                "role": "CAREGIVER",
                "username": "martinmueller_4",
                "monthly_working_hours": 80.0
            }
        },
        {
            "type": "User",
            "id": "caa9a1b2-3b78-43b2-8b66-f92f3f584a3a",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": "Herr",
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_3",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": "Mellinghoferstr.",
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": "16a",
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": "Oberhausen",
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": "46047",
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": "Seiteneingang",
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": "0151 123456789",
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": "0208 123456789",
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": "1992-11-10",
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "martin.mueller@testmail.com",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "Kommentar",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 80.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": "Herr",
                "lastname": "Müller",
                "firstname": "Martin",
                "street": "Mellinghoferstr.",
                "house_number": "16a",
                "city": "Oberhausen",
                "zip": "46047",
                "address_addition": "Seiteneingang",
                "phone_mobile": "0151 123456789",
                "phone_house": "0208 123456789",
                "birthday": "1992-11-10",
                "email": "martin.mueller@testmail.com",
                "comments": "Kommentar",
                "role": "CAREGIVER",
                "username": "martinmueller_3",
                "monthly_working_hours": 80.0
            }
        },
        {
            "type": "User",
            "id": "3c8a318d-2744-473d-abe4-e06c406b4136",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": "Herr",
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_2",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": "Mellinghoferstr.",
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": "16a",
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": "Oberhausen",
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": "46047",
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": "Seiteneingang",
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": "0151 123456789",
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": "0208 123456789",
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": "1992-11-10",
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "martin.mueller@testmail.com",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "Kommentar",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 80.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": "Herr",
                "lastname": "Müller",
                "firstname": "Martin",
                "street": "Mellinghoferstr.",
                "house_number": "16a",
                "city": "Oberhausen",
                "zip": "46047",
                "address_addition": "Seiteneingang",
                "phone_mobile": "0151 123456789",
                "phone_house": "0208 123456789",
                "birthday": "1992-11-10",
                "email": "martin.mueller@testmail.com",
                "comments": "Kommentar",
                "role": "CAREGIVER",
                "username": "martinmueller_2",
                "monthly_working_hours": 80.0
            }
        },
        {
            "type": "User",
            "id": "7acad2a8-0f4e-4c2d-a7b1-bfb699bcac36",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": "Herr",
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Müller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller_1",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": "Mellinghoferstr.",
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": "16a",
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": "Oberhausen",
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": "46047",
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": "Seiteneingang",
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": "0151 123456789",
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": "0208 123456789",
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": "1992-11-10",
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "martin.mueller@testmail.com",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "Kommentar",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 80.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": "Herr",
                "lastname": "Müller",
                "firstname": "Martin",
                "street": "Mellinghoferstr.",
                "house_number": "16a",
                "city": "Oberhausen",
                "zip": "46047",
                "address_addition": "Seiteneingang",
                "phone_mobile": "0151 123456789",
                "phone_house": "0208 123456789",
                "birthday": "1992-11-10",
                "email": "martin.mueller@testmail.com",
                "comments": "Kommentar",
                "role": "CAREGIVER",
                "username": "martinmueller_1",
                "monthly_working_hours": 80.0
            }
        },
        {
            "type": "User",
            "id": "eda14a0f-ca02-4a9a-9eb1-3d1edc7bfb87",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": "Herr",
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Mueller",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Martin",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "martinmueller",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": "Mellinghoferstr.",
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": "16a",
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": "Oberhausen",
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": "46047",
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": "Seiteneingang",
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": "0151 123456789",
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": "0208 123456789",
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": "1992-11-10",
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "martin.mueller@testmail.com",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "Kommentar",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 80.0,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": null,
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": null,
                "salutation": "Herr",
                "lastname": "Mueller",
                "firstname": "Martin",
                "street": "Mellinghoferstr.",
                "house_number": "16a",
                "city": "Oberhausen",
                "zip": "46047",
                "address_addition": "Seiteneingang",
                "phone_mobile": "0151 123456789",
                "phone_house": "0208 123456789",
                "birthday": "1992-11-10",
                "email": "martin.mueller@testmail.com",
                "comments": "Kommentar",
                "role": "CAREGIVER",
                "username": "martinmueller",
                "monthly_working_hours": 80.0
            }
        },
        {
            "type": "User",
            "id": "4297254b-51bb-4192-a2fc-649666e0d8b5",
            "attributes": {
                "field_values": [
                    {
                        "field_meta_data_id": 0,
                        "title": "salutation",
                        "value": null,
                        "position": 1,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "lastname",
                        "value": "Abdel Rehim",
                        "position": 2,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "firstname",
                        "value": "Faris",
                        "position": 3,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "username",
                        "value": "farisabdelrehim",
                        "position": 4,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "street",
                        "value": null,
                        "position": 5,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "house_number",
                        "value": null,
                        "position": 6,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "city",
                        "value": null,
                        "position": 7,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "zip",
                        "value": null,
                        "position": 8,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "address_addition",
                        "value": null,
                        "position": 9,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_mobile",
                        "value": null,
                        "position": 10,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "phone_house",
                        "value": null,
                        "position": 11,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "birthday",
                        "value": null,
                        "position": 12,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "email",
                        "value": "",
                        "position": 13,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "comments",
                        "value": "",
                        "position": 14,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "role",
                        "value": "CAREGIVER",
                        "position": 15,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "monthly_working_hours",
                        "value": 156.5,
                        "position": 16,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 0,
                        "title": "last_login",
                        "value": "2023-02-21T11:42:12.608638Z",
                        "position": 17,
                        "enums": null,
                        "placeholder": null,
                        "field_type": null,
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 2,
                        "title": "Service Level",
                        "value": null,
                        "position": 18,
                        "enums": "Premium, Standard, Basis",
                        "placeholder": null,
                        "field_type": "string - Dropdown",
                        "kind": "User"
                    },
                    {
                        "field_meta_data_id": 1,
                        "title": "Katzenhaarallergie",
                        "value": null,
                        "position": 19,
                        "enums": null,
                        "placeholder": null,
                        "field_type": "boolean - Checkbox",
                        "kind": "User"
                    }
                ],
                "last_login": "2023-02-21T12:42:12.608638+01:00",
                "salutation": null,
                "lastname": "Abdel Rehim",
                "firstname": "Faris",
                "street": null,
                "house_number": null,
                "city": null,
                "zip": null,
                "address_addition": null,
                "phone_mobile": null,
                "phone_house": null,
                "birthday": null,
                "email": "",
                "comments": "",
                "role": "CAREGIVER",
                "username": "farisabdelrehim",
                "monthly_working_hours": 156.5
            }
        }
    ]
}
```