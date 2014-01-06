=====
Photo
=====

Photos are at the heart of what Snapable is all about. Before we try uploading a
photo, we should look at how we can get data from the API.

Getting a Photo
===============

There are two parts to every photo:

- Metadata - *Information about the photo (ie. timestamp, caption, photographer, etc.)*
- Image - *The actual image data*

Metadata Request
----------------

The metadata around a photo is all the "extra stuff" about the photo that isn't the
actual photo data. It can contain everything from a caption to which event it is associated
with and when it was created.

**Request**:

.. code-block:: http

    GET /v1/photo/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "caption": "My Anonymous Photo.",
        "event": "/v1/event/1/",
        "guest": null,
        "resource_uri": "/v1/photo/1/",
        "created_at": "2013-06-20T03:35:56Z"
    }


Image Request
-------------

Having the metadata helps give context to the photo, but you also need the actual
photo data. You can get the actual JPEG photo data by using this request.

**Request**:

.. code-block:: http

    GET /v1/photo/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: image/jpeg
    Authorization: SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"

**Response**:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: image/jpeg

    än«–‚Lz…œZÕÛ˛cœzzœœZÕ2¨l$ºu¢≥“~:—UtI»›q©¿Ωn√Úeˇ\Vﬁ'öÒ¸õuÚPÇKco√≠aÏR—≥k'≤ˇ
    ...
    <more binary data here, humans can't read and understand this stuff>
    ...
    «Àü^æïÖOi)(ƒıpı0¥È^¢ªÙ¬PD∑”ÎF±XBÕ¥∑ÃÕm*zı§¿Á5üNæ7 ÇfÎ˝÷Ù´ñ◊1Ã°YWwP@ÎZ”
    «s√*Óç∆ÆI·óMº6ì1«ﬁäOQ

.. note::

    You would typically save the data returned from this API call directly into a file or display it to the
    user. How to display the raw binary data as an image depends on the programming language and environment
    used to interact with the API.

Getting a List of Photos
========================

You can get a list of photos using the ``/v1/photo/`` endpoint. This endpoint will
return all the photos in the system.

**Request:**

.. code-block:: http

    GET /v1/photo/ HTTP/1.1
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
            "total_count": 2
        },
        "objects": [
            {
                "caption": "My Anonymous Photo.",
                "event": "/v1/event/1/",
                "guest": null,
                "resource_uri": "/v1/photo/1/",
                "timestamp": "2013-06-20T03:35:56Z"
            },
            {
                "caption": "My photo of Michael.",
                "event": "/v1/event/2/",
                "guest": "/v1/guest/3/",
                "resource_uri": "/v1/photo/2/",
                "timestamp": "2013-06-20T03:34:11Z"
            }
        ]
    }

List of Photos for a Specific Event
-----------------------------------

A big list of all the photos in the system, is rarely useful. You are usually more interested
in a subset of all the photos. A typical scenario is getting a list of photos for a
particular event.

This can be accomplised by passing in a filtering option as part of the query. We
can filter the photos by the event id.

In this example we are only interested in the photos from the event with id ``2``, so we
add that to the ``GET`` parameters.

**Request:**

.. code-block:: http

    GET /v1/photo/?event=2 HTTP/1.1
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
            "total_count": 1
        },
        "objects": [
            {
                "caption": "My photo of Michael.",
                "event": "/v1/event/2/",
                "guest": "/v1/guest/3/",
                "resource_uri": "/v1/photo/2/",
                "timestamp": "2013-06-20T03:34:11Z"
            }
        ]
    }