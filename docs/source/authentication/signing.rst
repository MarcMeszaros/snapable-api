===============
Request Signing
===============

Each :term:`API` request must be authenticated. In order to do this, Snapable requires 
each :term:`API` request to be signed using the signing procedure below. The signing procedure
is loosely based on OAuth.

Build the RAW signature
-----------------------

The first step is to construct the signature is building the raw string to sign. It's as simple 
as concatenating various pieces of information.

.. cssclass:: table-bordered

+---------------+-------------------------------------------------------------------------------+
| Name          | Description                                                                   |
+===============+===============================================================================+
| api_key       | The *api_key* is the :term:`API` Key for access to the :term:`API`.           |
+---------------+-------------------------------------------------------------------------------+
| api_secret    | The *api_secret* is the :term:`API` secret for access to the :term:`API`.     |
+---------------+-------------------------------------------------------------------------------+
| verb          | The HTTP verb of the request type being made                                  |
|               | (**GET**/**POST**/**PUT**/**DELETE**).                                        |
|               |                                                                               |
|               | **NOTE: The verb must be uppercase.**                                         |
+---------------+-------------------------------------------------------------------------------+
| path          | The :term:`API` request path. The path of the request                         |
|               | *https://api.snapable.com/v1/photo/3/?streamable=1* would be */v1/photo/3/*   |
+---------------+-------------------------------------------------------------------------------+
| :term:`nonce` | A unique pseudo random string of lowercase alphanumeric characters generated  |
|               | for each :term:`API` request with a minimum length of 16 characters and a     |
|               | maximum length of 128 characters.                                             |
+---------------+-------------------------------------------------------------------------------+
| timestamp     | A UTC based unix timestamp. (ie: *1346531660*)                                |
|               |                                                                               |
|               | *NOTE: The API system uses*                                                   |
|               | `NTP <http://en.wikipedia.org/wiki/Network_Time_Protocol>`_                   |
|               | *to synchronize itself with UTC time. Request more than (+/-)120 seconds in   |
|               | variance from NTP based UTC time will be rejected.*                           |
+---------------+-------------------------------------------------------------------------------+

The preceding fields/data should be concatenated to create the raw signature string:

::

    raw_signature = api_key + verb + path + nonce + timestamp

Sign the RAW signature string
-----------------------------

The second step is to hash the signature using the `HMAC <http://en.wikipedia.org/wiki/Hash-based_message_authentication_code>`_ algorithm. The hashing algorithm to use 
is `SHA1 <http://en.wikipedia.org/wiki/SHA-1>`_. Sample hashing algorithms in various languages are provided below:

**Python**

.. code-block:: python
    :linenos:

    import hashlib
    import hmac

    api_key = 'abc123'
    api_secret = 'def789'
    verb = 'GET'
    path = '/v1/photo/3/'
    nonce = 'asd23eas12qwer89'
    timestamp = '1346531660'

    raw_signature = api_key + verb + path + nonce + timestamp

    signature = hmac.new(api_secret, raw_signature, hashlib.sha1).hexdigest()

**Ruby**

.. code-block:: ruby
    :linenos:

    require 'openssl'

    api_key = 'abc123'
    api_secret = 'def789'
    verb = 'GET'
    path = '/v1/photo/3/'
    nonce = 'asd23eas12qwer89'
    timestamp = '1346531660'

    raw_signature = api_key + verb + path + nonce + timestamp

    signature = Digest::HMAC.hexdigest(raw_signature, api_secret, Digest::SHA1)

**PHP**

.. code-block:: php
    :linenos:

    <?php
    // (PHP 5 >= 5.1.2, PECL hash >= 1.1)
    $api_key = 'abc123';
    $api_secret = 'def789';
    $verb = 'GET';
    $path = '/v1/photo/3/';
    $nonce = 'asd23eas12qwer89';
    $timestamp = '1346531660';

    $raw_signature = $api_key . $verb . $path . $nonce . $timestamp;

    $signature = hash_hmac('sha1', $raw_signature, $api_secret);


Create the Authorization header
-------------------------------

The third and final step is to build the **Authorization** header. The authorization header 
needs the following:

.. code-block:: python

    # SNAP key="<api_key>",signature="<hexdigest_signature>",nonce="<nonce>",timestamp="<timestamp>"

    SNAP key="abc123",signature="129e...4696",nonce="asd23eas12qwer89",timestamp="1346531660"

.. note::
    
    Part of the authorization string has been replaced with "..." to keep the example code shorter.

The resulting string goes into the **Authorization** HTTP header. 