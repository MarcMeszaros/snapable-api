====
User
====

The system is only useful if there are users to interact with it. A user can be 
thought of as an event organizer.

Creating a User
===============

Let's start by veryfying how many users exist in the system.

**Request**:

.. code-block:: http

    GET /v1/user/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "meta": {
            "limit": 50,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 0
        },
        "objects": []
    }

Just as we expect, there are no users. The first step is to create a new user.

**Request**:

.. code-block:: http

    POST /v1/user/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Content-Type: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

    {
        "email": "michael@example.com",
        "password": "monkey123",
        "first_name": "Michael",
        "last_name": "Bluth"
    }

**Response**:

.. code-block:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "accounts": [
            "/v1/account/1/"
        ],
        "email": "michael@example.com",
        "password": "monkey123",
        "first_name": "Michael",
        "last_name": "Bluth",
        "resource_uri": "/v1/user/1/"        
    }

We should now have one user if we try to list all the users.

**Request**:

.. code-block:: http

    GET /v1/user/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "meta": {
            "limit": 50,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 0
        },
        "objects": [
            {
                "accounts": [
                    "/v1/account/1/"
                ],
                "email": "michael@example.com",
                "first_name": "Michael",
                "last_name": "Bluth",
                "resource_uri": "/v1/user/1/"
            }
        ]
    }

We can also get the details of the specific user we just created.

**Request**:

.. code-block:: http

    GET /v1/user/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "accounts": [
            "/v1/account/1/"
        ],
        "email": "michael@example.com",
        "first_name": "Michael",
        "last_name": "Bluth",
        "resource_uri": "/v1/user/1/"        
    }

Updating a User
===============

We realized we made a mistake in the name while creating the user. No problem, we can just update the user.

**Request**:

.. code-block:: http

    PUT /v1/user/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Content-Type: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

    {
        "email": "michael@example.com",
        "first_name": "Michael",
        "last_name": "Bluth"
    }

**Response**:

.. code-block:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json

    {
        "accounts": [
            "/v1/account/1/"
        ],
        "email": "michael@example.com",
        "first_name": "Michael",
        "last_name": "Bluth",
        "resource_uri": "/v1/user/1/"
    }

We can verify the user to make sure our changes were accepted.

**Request**:

.. code-block:: http

    GET /v1/user/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "accounts": [
            "/v1/account/1/"
        ],
        "email": "michael@example.com",
        "first_name": "Michael",
        "last_name": "Bluth",
        "resource_uri": "/v1/user/1/"
    }