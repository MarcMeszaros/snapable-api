.. _partner_v1-account:

=======
Account
=======

The *account* resource is the root resource that all others lead back to. An 
*account* is automatically created when a :ref:`user <partner_v1-user>` resource
is created. In most cases, you don't need to worry about the account. It is included
since more features may be added to it in the future.

.. Read
.. ----

.. http:get:: /partner_v1/account/

  The list of all accounts.

  **Example request**:

  .. sourcecode:: http

    GET /partner_v1/account/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json


  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
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
          "resource_uri": "/partner_v1/account/1/",
          "users": [
            "/partner_v1/user/1/"
          ]
        }
      ]
    }

  :status 200: no error

.. http:get:: /partner_v1/account/(account_id)/

  Details about a specific account.

  **Example request**:

  .. sourcecode:: http

    GET /partner_v1/account/1/ HTTP/1.1
    Host: api.snapable.com
    Accept: application/json


  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
      "resource_uri": "/partner_v1/account/1/",
      "users": [
        "/partner_v1/user/1/"
      ]
    }

  :param account_id: the id of the account to get

  :status 200: no error
