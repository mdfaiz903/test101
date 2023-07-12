# Database


1. [Overview](#Overview)
2. [Tables](#Tables)

## Overview


This is a concise overview of the project tables. 

|Nr|Title|Description|Table-Name|Implemented?|
|---|---|---|---|---|
|1|**Customers**|Contains the fixed base fields for customers|*customers*|Yes|
|2|**Users**|Contains the fixed base fields for employees|*users*|Yes|
|...|**...**|...|...|...|

## Tables

In the following, all project tables are named and their fields are listed in detail. The data types are named according to the Django Model field reference.

### Customers

Contains the fixed base fields for customers:

**Fields** 

|Name|Description|Datatype|
|---|---|---|
|*id*|Unique ID|UUIDField|
|*salutation*|Salutation|CharField|
|*lastname*|Last Name|CharField|
|*firstname*|First Name|CharField|
|*street*|Street|CharField|
|*house_number*|House Number|CharField|
|*city*|City|CharField|
|*zip*|ZIP Code|IntegerField|
|*address_addition*|Additional information to the address|TextField|
|*phone_primary*|Primary Phone Number|CharField|
|*phone_secondary*|Secondary Phone Number|CharField|
|*birthday*|Date of Birth|DateField|
|*email*|E-Mail Adresse|EmailField|

**Example** 
|id|salutaton|lastname|firstname|street|house_number|city|zip|address_addition|birthday|phone_primary|phone_secondary|email|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|...|...|...|...|...|...|...|...|...|...|...|...|...|
|3cd2...|Herr|Mustermann|Max|Musterstraße|10|Essen|45127|5. Stock|01.01.1950|0201 123456789|0151 123456789|m.mustermann@gmx.de|
|...|...|...|...|...|...|...|...|...|...|...|...|...|

### Customer-Custom-Fields-Description

Contains the additional fields for customers:

**Fields** 

TBD

Possible datatypes: [IntegerField], [CharField], [DateField] 

**Example** 

TBD

### TBD