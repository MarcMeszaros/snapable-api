==============
Authentication
==============

Each API request must be authenticated. In order to do this, Snapable requires 
each API request to be signed.

Required Header Fields
----------------------

The following fields must be included in every authenticated API request:

- Authorization

Signing Requests
----------------

There are a few steps required in signing an API request, but essentially there are only 3 steps.

Step 1 - Build the RAW signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to construct the signature is building the raw string to sign. It's as simple 
as concatenating various pieces of information.

.. cssclass:: table-bordered

==============  =============================================================================
Name            Description
==============  =============================================================================
api_key         The *api_key* is the API Key for access to the Snapable API.

api_secret      The *api_secret* is the API secret for access to the Snapable API.

verb            The HTTP verb of the request type being made 
                (**GET**/**POST**/**PUT**/**DELETE**).

                **NOTE: The verb must be uppercase.**

path            The API request path. The path of the request 
                *https://api.snapable.com/v1/photo/3/?streamable=1* would be */v1/photo/3/*

nonce           A unique pseudo random string of lowercase alphanumeric characters generated 
                for each API request with a minimum length of 16 characters and a maximum 
                length of 128 characters.

timestamp       A UTC based unix timestamp. (ie: *1346531660*)
==============  =============================================================================

The preceding fields/data should be concatenated to create the raw signature string:

::

    raw_signature = api_key + verb + path + nonce + timestamp

Step 2 - Sign the RAW signature string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second step is to hash the signature using the `HMAC <http://en.wikipedia.org/wiki/Hash-based_message_authentication_code>`_ algorithm. The hashing algorithm to use 
is SHA1. Sample hashing algorithms in various languages are provided below:

**Python**

.. code-block:: python
    :linenos:

    import hashlib
    import hmac

    api_key = 'abc123'
    api_secret = 'def789'
    verb = 'GET'
    path = '/v1/photo/3/'
    x_snap_nonce = 'asd23eas'
    x_snap_timestamp = '1346531660'

    raw_signature = api_key + verb + path + x_snap_nonce + x_snap_timestamp

    signature = hmac.new(api_secret, raw_signature, hashlib.sha1)

**PHP**

.. code-block:: php
    :linenos:
    
    // (PHP 5 >= 5.1.2, PECL hash >= 1.1)
    $api_key = 'abc123';
    $api_secret = 'def789';
    $verb = 'GET';
    $path = '/v1/photo/3/';
    $x_path_nonce = 'asd23eas';
    $x_snap_date = '1346531660';

    $raw_signature = $api_key . $verb . $path . $x_snap_nonce . $x_snap_timestamp;

    $signature = hash_hmac('sha1', $raw_signature, $api_secret);


Step 3 - Create the Authorization header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The third and final step is to build the Authorization header. The authorization header 
needs the following:

::

    # SNAP snap_key="<api_key>",snap_signature="<hexdigest_signature>",snap_nonce="<nonce>",snap_timestamp="<timestamp>"

    SNAP snap_key="abc123",snap_signature="af687fa53e743676a5e9b4880e8762919ba17637",snap_nonce="asd23eas",snap_timestamp="1346531660"

The resulting string goes into the *Authorization* HTTP header. 