# DELETE USER

Endpoint: <code>/api/users/:\<uuid></code>  (POST)

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
|type|String|Yes|User type <br>(Choices: "CAREGIVER", "SUPERVISOR", "CEO", "ADMIN")|

## EXAMPLES

### Minimum required fields

#### Create Caregiver
```yaml
{
    "data":{
        "type":"User",
        "attributes":{
            "lastname": "Mueller",
            "firstname": "Martin",
            "password": "testpasswort",
            "type":"CAREGIVER"
        }
    }
}


-Server response (201 CREATED)-
{
    "data": {
        "type": "User",
        "id": "0838e728-3137-4fe9-b5d4-f7ed7541ec03",
        "attributes": {
            "field_values": [
                {
                    "field_meta_data_id": 2,
                    "title": "Service Level",
                    "value": null,
                    "position": 2,
                    "enums": "Premium, Standard, Basis",
                    "placeholder": null,
                    "field_type": "string - Dropdown",
                    "kind": "User"
                },
                {
                    "field_meta_data_id": 1,
                    "title": "Katzenhaarallergie",
                    "value": null,
                    "position": 1,
                    "enums": null,
                    "placeholder": null,
                    "field_type": "boolean - Checkbox",
                    "kind": "User"
                }
            ],
            "password": "pbkdf2_sha256$390000$dnmK6ooArZ6G4xZIN67atO$jhImEtwELU0u/sN0daU3lOg/MsPbMqSjLRb3fPaLaHo=",
            "last_login": null,
            "date_joined": "2023-02-22T09:44:38.262174+01:00",
            "salutation": null,
            "lastname": "Mueller",
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
            "deleted": false,
            "deleted_at": null,
            "type": "CAREGIVER",
            "username": "martinmueller",
            "monthly_working_hours": 160.0,
            "created_at": "2023-02-22T09:44:38.344542+01:00",
            "modified_at": "2023-02-22T09:44:38.344552+01:00",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "invalidate_before": null
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
            "lastname": "Mueller",
            "firstname": "Martin",
            "password": "testpasswort",
            "type": "ADMIN"
        }
    }
}

-Server response (201 CREATED)-
{
    "data": {
        "type": "User",
        "id": "5ed266af-7e95-4438-8e56-60890cba36b4",
        "attributes": {
            "field_values": [
                {
                    "field_meta_data_id": 2,
                    "title": "Service Level",
                    "value": null,
                    "position": 2,
                    "enums": "Premium, Standard, Basis",
                    "placeholder": null,
                    "field_type": "string - Dropdown",
                    "kind": "User"
                },
                {
                    "field_meta_data_id": 1,
                    "title": "Katzenhaarallergie",
                    "value": null,
                    "position": 1,
                    "enums": null,
                    "placeholder": null,
                    "field_type": "boolean - Checkbox",
                    "kind": "User"
                }
            ],
            "password": "pbkdf2_sha256$390000$7uhjsgyoxuleN9kYBlDRy1$4ljbKXPrLVppignGUBQm1dXWvEA6CC3OSgZPGBG/TqY=",
            "last_login": null,
            "date_joined": "2023-02-22T09:45:59.311755+01:00",
            "salutation": null,
            "lastname": "Mueller",
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
            "deleted": false,
            "deleted_at": null,
            "type": "ADMIN",
            "username": "martinmueller",
            "monthly_working_hours": 160.0,
            "created_at": "2023-02-22T09:45:59.403453+01:00",
            "modified_at": "2023-02-22T09:45:59.403461+01:00",
            "is_active": true,
            "is_staff": true,
            "is_superuser": true,
            "invalidate_before": null
        }
    }
}
```


### All fields without custom fields
```yaml
{
    "data": {
        "type": "User",
        "attributes": {
            "lastname": "Mueller",
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
            "type": "CAREGIVER",
            "monthly_working_hours": 80.0
        }
    }
}

-Server response (201 CREATED)-
{
    "data": {
        "type": "User",
        "id": "3d3f426c-aa8c-4927-98f4-67a87f0bbbf0",
        "attributes": {
            "field_values": [
                {
                    "field_meta_data_id": 2,
                    "title": "Service Level",
                    "value": null,
                    "position": 2,
                    "enums": "Premium, Standard, Basis",
                    "placeholder": null,
                    "field_type": "string - Dropdown",
                    "kind": "User"
                },
                {
                    "field_meta_data_id": 1,
                    "title": "Katzenhaarallergie",
                    "value": null,
                    "position": 1,
                    "enums": null,
                    "placeholder": null,
                    "field_type": "boolean - Checkbox",
                    "kind": "User"
                }
            ],
            "password": "pbkdf2_sha256$390000$GGlmTRilGsV420xY3NwJ1P$5aSrt9+frtB/QcbLJaNUG2TMcgCcgYHyyLahA/ptpTA=",
            "last_login": null,
            "date_joined": "2023-02-22T09:46:28.514889+01:00",
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
            "deleted": false,
            "deleted_at": null,
            "type": "CAREGIVER",
            "username": "martinmueller",
            "monthly_working_hours": 80.0,
            "created_at": "2023-02-22T09:46:28.605056+01:00",
            "modified_at": "2023-02-22T09:46:28.605065+01:00",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "invalidate_before": null
        }
    }
}
```

### All fields with custom fields

```yaml
{
    "data": {
        "type": "User",
        "attributes": {
            "field_values": [
                {
                    "field_meta_data_id": 2,
                    "title": "Service Level",
                    "value": "Standard",
                    "position": 2,
                    "enums": "Premium, Standard, Basis",
                    "placeholder": null,
                    "field_type": "string - Dropdown",
                    "kind": "User"
                },
                {
                    "field_meta_data_id": 1,
                    "title": "Katzenhaarallergie",
                    "value": "1",
                    "position": 1,
                    "enums": null,
                    "placeholder": null,
                    "field_type": "boolean - Checkbox",
                    "kind": "User"
                }
            ],            
            "lastname": "Mueller",
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
            "type": "CAREGIVER",
            "monthly_working_hours": 80.0
        }
    }
}

-Server response (201 CREATED)-
{
    "data": {
        "type": "User",
        "id": "9f32210a-64e4-43bb-a1ef-092b9ef91549",
        "attributes": {
            "field_values": [
                {
                    "field_meta_data_id": 2,
                    "title": "Service Level",
                    "value": "Standard",
                    "position": 2,
                    "enums": "Premium, Standard, Basis",
                    "placeholder": null,
                    "field_type": "string - Dropdown",
                    "kind": "User"
                },
                {
                    "field_meta_data_id": 1,
                    "title": "Katzenhaarallergie",
                    "value": "1",
                    "position": 1,
                    "enums": null,
                    "placeholder": null,
                    "field_type": "boolean - Checkbox",
                    "kind": "User"
                }
            ],
            "password": "pbkdf2_sha256$390000$lWmTgDefCDyG9YkK9a60DB$XM6/+FFYktJqWI+SfB9NaM2PI86EJUAhkgJkWDDyvEg=",
            "last_login": null,
            "date_joined": "2023-02-22T09:53:55.323126+01:00",
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
            "deleted": false,
            "deleted_at": null,
            "type": "CAREGIVER",
            "username": "martinmueller",
            "monthly_working_hours": 80.0,
            "created_at": "2023-02-22T09:53:55.410231+01:00",
            "modified_at": "2023-02-22T09:53:55.410241+01:00",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "invalidate_before": null
        }
    }
}
```