==============
Authentication
==============

Before any :term:`API` call can be made, some basic authentication code needs to
be setup. The API requires every request to be signed by an API key and secret.
The current signing algorithm is `HMAC <https://en.wikipedia.org/wiki/Hash-based_message_authentication_code>`_ 
based and is loosely inspired by OAuth. *This current signing algoritm may be deprecated 
and replaced in the future in favor of a more standardized authorization algorithm.*

The best way to understand the signing algoritm is by following an example. Suppose 
we want to sign the following GET request: ``https://api.snapable.com/v1/photo/3/?streamable=1``

Raw Signature
=============

When signing the request, data from the request is used for the signing algorithm. 
Various parts of the API request are assembles into a string and that string is signed. 
The signature is sent with the request and the server verifies the request by 
calculating the signature itself and comparing it with the one sent in the request.

The various parts required are specified in signing algorithm documentation 
[:doc:`/authentication/signing`]. The raw signature string is composed of various
data from the request.

.. code-block:: python
    
    raw_signature = api_key + HTTP verb + path + nonce + timestamp


We start by using the HTTP verb and path from the request and add it to our raw string.

.. code-block:: python
    
    raw_signature = api_key + 'GET' + '/v1/photo/3/' + nonce + timestamp

A :term:`nonce` is a random string of charaters and numbers used by the :term:`API`
for security purposes.

.. code-block:: python
    
    raw_signature = api_key + 'GET' + '/v1/photo/3/' + 'asd23eas12qwer89' + timestamp

The timestamp is used to tell the server when the request was sent. It is a UTC based
unix timestamp.

.. code-block:: python

    raw_signature = api_key + 'GET' + '/v1/photo/3/' + 'asd23eas12qwer89' + '1346531660'

Finally the API key is added to the string.

.. code-block:: python
    
    # raw string with all the parts
    raw_signature = 'abc123' + 'GET' + '/v1/photo/3/' + 'asd23eas12qwer89' + '1346531660'

    # raw string with the parts concatenated
    raw_signature = 'abc123GET/v1/photo/3/asd23eas12qwer891346531660'

Signing
=======

Now that we have our raw signature string we need to actually sign it with the API secret.
Implementation details vary for each language. Some sample code for a few languages
is provided on the [:doc:`/authentication/signing`] page.

**Python**

.. code-block:: python
    :linenos:

    import hashlib
    import hmac

    api_secret = 'def789'
    raw_signature = 'abc123GET/v1/photo/3/asd23eas12qwer891346531660'

    signature = hmac.new(api_secret, raw_signature, hashlib.sha1).hexdigest()
    # signature = 129ed706d8fcb3ba864b0784d3f4c792eaa64696

**Ruby**

.. code-block:: ruby
    :linenos:

    require 'openssl'

    api_secret = 'def789'
    raw_signature = 'abc123GET/v1/photo/3/asd23eas12qwer891346531660'

    signature = Digest::HMAC.hexdigest(raw_signature, api_secret, Digest::SHA1)
    # signature = 129ed706d8fcb3ba864b0784d3f4c792eaa64696

**PHP**

.. code-block:: php
    :linenos:

    <?php
    // (PHP 5 >= 5.1.2, PECL hash >= 1.1)
    $api_secret = 'def789';
    $raw_signature = 'abc123GET/v1/photo/3/asd23eas12qwer891346531660';
    
    $signature = hash_hmac('sha1', $raw_signature, $api_secret);
    // signature = 129ed706d8fcb3ba864b0784d3f4c792eaa64696

HTTP Header
===========

Once the signature has been calculated for the request, it must be included in the
**Authorization** header. The header includes the following values:

- API Key
- signature hexdigest
- nonce
- timestamp

The entire authorization string has the format:

::

    # Format:
    # SNAP key="<api_key>",signature="<hexdigest_signature>",nonce="<nonce>",timestamp="<timestamp>"

    # the authorization string to be inserted into the header
    auth_string = 'SNAP key="abc123",signature="129e...4696",nonce="asd...r89",timestamp="1346531660"'

.. note::
    
    Part of the authorization string has been replaced with "..." to keep the example code shorter.

The entire authorization string is then added to the **Authorization** header.