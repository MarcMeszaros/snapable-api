=====
Guest
=====

Each event can have multiple guests taking photos. A guest is not required to be associated
to a photo, but if there is, it can give more context to the photo.

Creating a Guest
================

Guests are very simple resources and only contain a few fields.

**Request**:

.. code-block:: http

    POST /v1/guest/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Content-Type: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

    {
        "event": "/v1/event/1/",
        "email": "gob@example.com",
        "name": "GOB"
    }

**Response**:

.. code-block:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "email": "gob@example.com",
        "event": "/v1/event/1/",
        "name": "GOB",
        "resource_uri": "/v1/guest/3/"
    }
