# API Design

## Overview on HTTP Methods

|Purpose of Request|HTTP Method|Rough SQL Equivalent|
|---|---|---|
|Create a new resource|**POST**|INSERT|
|Read an existing resource|**GET**|SELECT|
|Update an existing resource (completely)|**PUT**|UPDATE|
|Update an existing resource (partially)|**PATCH**|UPDATE|
|Delete an existing resource|**DELETE**|DELETE|

## API Endpoints (Overview)

<!--<details> </details>-->
<summary><b><code>/api/customers</b></code></summary>
<br>
<code><b>POST</b></code><code>Create new customer</code>  

### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | `data`      |  `required` | `JSON`  | {<br>`"lastname":"Mueller"`,<br>`"firstname":"Martin"`,<br>...<br>`"has_car":true`<br>}  |   

### Response

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `201`         | `TBD: text/plain;charset=UTF-8`        | `Customer created successfully`                                |
> | `400`         | `TBD: application/json`                | `{"code":"400","message":"Bad Request"}`                            |
> | `401`         | `TBD: application/json`                | `{"code":"403","message":"Authentication required but user did not provie credentials or provided invalid ones"}`                            |
<br> 
&emsp;<code><b>GET</b></code><code>Get list of Customers</code>