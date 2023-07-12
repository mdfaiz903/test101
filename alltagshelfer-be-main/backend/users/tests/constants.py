from dataclasses import dataclass


TEST_CAREGIVER = {
    'salutation': "Herr",
    'firstname': "Jürgen",
    'lastname': "Schmidt",
    'password': "password_caregiver_schmidt"
}

TEST_CAREGIVER_OUTPUTS = {
    'username': 'juergenschmidt'
}

TEST_SUPERVISOR = {
    'salutation': "Frau",
    'firstname': "Sümeyra",
    'lastname': "Yilmaz",
    'password': "password_supervisor_yilmaz",
    'role': 'SUPERVISOR'
}

TEST_SUPERVISOR_OUTPUTS = {
    'username': 'suemeyrayilmaz'
}

TEST_CEO = {
    'salutation': "Herr",
    'firstname': "Farid",
    'lastname': "Allam",
    'password': "password_ceo_allam",
    'role': 'CEO'
}

TEST_CEO_OUTPUTS = {
    'username': 'faridallam'
}

TEST_ADMIN = {
    'salutation': "Frau",
    'firstname': "Melanie",
    'lastname': "Maximum",
    'password': "password_admin_maximum",
    'role': 'ADMIN'
}

TEST_ADMIN_OUTPUTS = {
    'username': 'melaniemaximum'
}
