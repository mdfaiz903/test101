# API Design

<br>

## Overview on HTTP Methods

|Purpose of Request|HTTP Method|Rough SQL Equivalent|
|---|---|---|
|Create a new resource|**POST**|INSERT|
|Read an existing resource|**GET**|SELECT|
|Update an existing resource (completely)|**PUT**|UPDATE|
|Update an existing resource (partially)|**PATCH**|UPDATE|
|Delete an existing resource|**DELETE**|DELETE|

<br>

## Utilized HTTP Status Codes

|Status Code|HTTP Method|Type|Information|
|---|---|---|---|
|200 (OK)|GET|**Success**|The resource has been fetched and transmitted in the message body|
|200 (OK)|PUT/PATCH|**Success**|The resource has been modified and transmitted in the message body|
|201 (Created)|POST|**Success**|The resource has succeeded, and a new resource was created as a result.|
|204 (No Content)|DELETE|**Success**|There is no content for this request - the deletion was successful.|
|400 (Bad Request)|GET/PUT/PATCH/DELETE|**Error**|The server cannot or will not process the request due to something that is perceived to be a client error.|
|404 (Not Found)|GET/PUT/PATCH/DELETE|**Error**|The server cannot find the requested resource.|
|409 (Conflict)|PATCH|**Error**|This response is sent when a request conflicts with the current state of the server.|


## API Endpoints (Overview)

---

<summary><b><code>/api/customers/</b></code></summary>
<br>
<summary><code><b>GET</b></code><code>List all Customers</code>  </summary>
<br>
<summary><code><b>POST</b></code><code>Create new customer</code>  </summary> 

---

<summary><b><code>/api/customers/:uuid/</b></code></summary>
<br>
<summary><code><b>GET</b></code><code>View Customer</code>  </summary>
<br>
<summary><code><b>PUT</b></code><code>Update Customer</code>  </summary>
<br>
<summary><code><b>PATCH</b></code><code>Update Customer partially</code>  </summary>
<br>
<summary><code><b>DELETE</b></code><code>Delete Customer</code>  </summary>

---

<summary><b><code>/api/users/</b></code></summary>
<br>
<summary><code><b>GET</b></code><code>List all Users</code>  </summary>
<br>
<summary><code><b>POST</b></code><code>Create new User</code>  </summary> 

---

<summary><b><code>/api/users/:uuid/</b></code></summary>
<br>
<summary><code><b>GET</b></code><code>View User</code>  </summary>
<br>
<summary><code><b>PUT</b></code><code>Update User</code>  </summary>
<br>
<summary><code><b>PATCH</b></code><code>Update User partially</code>  </summary>
<br>
<summary><code><b>DELETE</b></code><code>Delete User</code>  </summary>
