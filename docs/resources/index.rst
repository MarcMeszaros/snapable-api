=============
API Resources
=============

The Snapable :term:`API` resources are what developers will be interacting with
most. They represent various pieces of data the :term:`API` makes available to 
developers. Like any :term:`API` there are always some caveats, which are 
explained and documented in further in this section.

**Base URL**

There are two distinct copies of the API. One is used for testing/development of your
application and the second is the live production version. You should use the 
development environment when create your application and the live version when you
release to your users.

*Both environments are completely seperate and no data is shared between them. API
keys for the development environment will not work on the live environment.*

    **Live** 

    ``https://api.snapable.com/``

    **Testing/Development**

    ``https://devapi.snapable.com/``

    *NOTE: Because this is a testing environment, API data may be deleted periodically.*

**API Version**

Like any other piece of software API's change. When a non backwards compatible 
change to the API is made, the version number will be increased. The API version
number is included in all requests and is part of the request URL. It is the first
part of the URI.

*At this time, there is only one semi-public* :term:`API` *available to partners.*

*Example*

In ``https://api.snapable.com/v1/photo/3/``, **v1** is the API Version.

===========
Data Format
===========

By default the data returned from :term:`API` calls is of type :mimetype:`application/json`. In
certain circumstances the ``Accept`` header needs to be overriden to get a 
different data format.

*meta* section
==============

The ``meta`` section in API responses is used when calling an endpoint which
contains a list of results. It contains some meta information about the particular
request executed.

- ``limit`` - the number of objects on a response "page"
- ``next`` - the uri for the next "page"
- ``offset`` - the current offset of objects
- ``previous`` - the uri for the previous "page"
- ``total_count`` - the total number of objects returned

**Examples**

::

    {
        "meta": {
            "limit": 50,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 8
        },
        "objects": [
            ...
        ]
    }

::

    {
        "meta": {
            "limit": 50,
            "next": "/v1/account/?limit=50&offset=50",
            "offset": 0,
            "previous": null,
            "total_count": 100
        },
        "objects": [
            ...
        ]
    }

*resource_uri* field
====================

The ``resource_uri`` field is similar to what would be considered and "id" field
except that the it is the full uri representation of the resource. You will see
this field throught the Snapable :term:`API`. If you really only need the "id", you can
get the substring that only contains the id.

::

    {
        "meta": {
            ...
        },
        "objects": [
            {
                ...
                "resource_uri": "/v1/account/1/",
                ...
            },
            {
                ...
                "resource_uri": "/v1/account/2/",
                ...
            }
        ]
    }

*Accept* Header
===============

By default the API returns data in :term:`JSON` format if the **Accept** HTTP header
is not set. You can explicitly set the header to :mimetype:`application/json` if 
you want.

Some resource endpoints can handle different **Accept** headers as well.

*Photo* Resource
------------------

The photo resource also will also allow :mimetype:`image/jpeg` 
in the **Accept** header. This will return the raw binary JPEG image data of the 
specified photo resource. Some extra parameter are also read from the request when 
processing the request such as the ``size`` query parameter.

*Content-Type* Header
=====================

When submitting a request with :term:`JSON` data in the body, the **Content-Type** should be
set to use :mimetype:`application/json`.

**Exception**

When uploading a photo, the body data should be encoded 
using :mimetype:`multipart/form-data` as defined in :rfc:`2388`. The **Content-Type** 
header should be set to :mimetype:`multipart/form-data`.