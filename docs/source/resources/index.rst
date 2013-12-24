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

.. toctree::
    :maxdepth: 1

    data
    partner_v1/index