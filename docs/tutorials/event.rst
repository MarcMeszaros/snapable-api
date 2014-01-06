=====
Event
=====

Having a user in the Snapable system is nice, but not very useful unless they have
an event to upload photos too.

Creating an Event
=================

Only a subset of the data is required when creating an event. Some of the data is
generated automatically (ie. pin). Below is an example of how to create an event with
the basic information that is required.

**Request**:

.. code-block:: http

    POST /v1/user/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Content-Type: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

    {
        "account": "/v1/account/1/",
        "end_at": "2013-06-21T00:00:00Z",
        "start_at": "2013-06-20T00:00:00Z",
        "title": "Awesome",
        "url": "awesome-event",
        "is_public": "true",
        "tz_offset": -240
    }

**Response**:

.. code-block:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "account": "/v1/account/1/",
        "is_enabled": true,
        "end_at": "2013-06-21T00:00:00Z",
        "locations": [],
        "photo_count": 0,
        "pin": "8092",
        "is_public": true,
        "resource_uri": "/v1/event/1/",
        "start_at": "2013-06-20T00:00:00Z",
        "title": "Awesome",
        "tz_offset": -240,
        "url": "awesome-event"
    }

Creating a Location
-------------------

You may have noticed a ``locations`` field in the event response. Events can specify
physical locations where the event is taking place. This information is useful in certain
situations (ie. "Nearby Events" using GPS on a phone for example).

**Request**:

.. code-block:: http

    POST /v1/location/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Content-Type: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

    {
        "address": "1 Lucille Lane, Sudden Valley, California, United States",
        "event": "/v1/event/1/",
        "lat": "33.640800",
        "lng": "-117.603100",
    }

**Response**:

.. code-block:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "address": "1 Lucille Lane, Sudden Valley, California, United States",
        "event": "/v1/event/1/",
        "lat": "33.640800",
        "lng": "-117.603100",
        "resource_uri": "/v1/location/1/"
    }

Now that, the event has a location, it will show up when we get the event details.

**Request**:

.. code-block:: http

    GET /v1/event/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "account": "/v1/account/1/",
        "is_enabled": true,
        "end_at": "2013-06-21T00:00:00Z",
        "locations": [
            {
                "address": "1 Lucille Lane, Sudden Valley, California, United States",
                "event": "/v1/event/1/",
                "lat": "33.640800",
                "lng": "-117.603100",
                "resource_uri": "/v1/location/1/"
            }
        ],
        "photo_count": 41,
        "pin": "8092",
        "is_public": true,
        "resource_uri": "/v1/event/2/",
        "start_at": "2013-06-20T00:00:00Z",
        "title": "Awesome",
        "tz_offset": 0,
        "url": "awesome-event"
    }
