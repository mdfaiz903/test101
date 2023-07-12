# CREATE USER

Endpoint: <code>/api/users/</code>  (POST)

## REQUEST HEADER
|Key|Value|
|-|-|
|Content-Type|application/vnd.api+json|
|Authorization|Bearer \<token>|

## REQUIRED FIELDS
|Field|Type|Required|Content|
|-|-|-|-|
|lastname|String|Yes|Last Name|
|firstname|String|Yes|First Name|
|password|String|Yes|Password|
|role|String|Yes|User type <br>(Choices: "CAREGIVER", "SUPERVISOR", "CEO", "ADMIN")|

## EXAMPLES

### Minimum required fields

#### Create Caregiver
```yaml
{
    "data":{
        "type":"User",
        "attributes":{
            "lastname": "Müller",
            "firstname": "Martin",
            "password": "testpasswort",
            "role": "CAREGIVER"
        }
    }
}


-Server response (201 CREATED)-
{
    "data": {
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
                    "value": 160,
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
            "username": "martinmueller_6"
        }
    }
}
```

### Create Admin
```yaml
{
    "data":{
        "type":"User",
        "attributes":{
            "lastname": "Müller",
            "firstname": "Martin",
            "password": "testpasswort",
            "role": "ADMIN"
        }
    }
}

-Server response (201 CREATED)-
{
    "data": {
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
                    "value": 160,
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
    }
}
```


### All fields
```yaml
{
    "data": {
        "type": "User",
        "attributes": {
            "lastname": "Müller",
            "firstname": "Martin",
            "password": "testpassword",            
            "salutation": "Herr",            
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
        }
    }
}

-Server response (201 CREATED)-
{
    "data": {
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
    }
}
```