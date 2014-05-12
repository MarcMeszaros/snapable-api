FORMAT: 1A
HOST: https://api.snapable.com/partner_v1/

# Snapable Partner API (v1)
The partner API gives developers access to the Snapable backend allowing them
to create events and accounts from their own application.

To get more information about getting an API key, please contact us.

# Group Accounts
The account resource is the root resource that all others lead back to. An 
account is automatically created when a user resource is created. In most cases, 
you don't need to worry about the account. It is included since more features 
may be added to it in the future.

## Account List [/account/]
Account list description

+ Model (application/json)
    + Body

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

### Get Accounts [GET]
The list of all accounts.

+ Response 200
    [Account List][]

## Account [/account/{id}/]
Account description

+ Parameters
    + id (required, integer, `1`) ... The account id

+ Model (application/json)
    + Body

            {
                "resource_uri": "/partner_v1/account/1/",
                "users": [
                    "/partner_v1/user/1/"
                ]
            }

### Get Account [GET]
Details about a specific account.

+ Response 200

    [Account][]

# Group Events
The *event* resource is one of the core resources available via the API. It contains
various information about the event such as the event title, the start and end time
of the event and other information.

## Event List [/event/]

+ Model (application/json) 

    + Body

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
                        "account": "/partner_v1/account/1/",
                        "is_enabled": true,
                        "end_at": "2013-06-21T00:00:00Z",
                        "locations": [
                            {
                                "address": "1 Lucille Lane, Sudden Valley, California, United States",
                                "event": "/partner_v1/event/1/",
                                "lat": "33.640800",
                                "lng": "-117.603100",
                                "resource_uri": "/partner_v1/location/1/"
                            }
                        ],
                        "photo_count": 41,
                        "pin": "1234",
                        "is_public": false,
                        "resource_uri": "/partner_v1/event/2/",
                        "start_at": "2013-06-20T00:00:00Z",
                        "title": "Awesome",
                        "tz_offset": 0,
                        "url": "awesome-event"
                    }
                ]
            }

### Get Events [GET]
The list of all accounts.

+ Response 200
    [Event List][]

### Create Event [POST]
Create an event. The event url must be unique.

+ Request (application/json)
    + Body

            {
                "account": "/partner_v1/account/1/",
                "end_at": "2013-06-21T00:00:00Z",
                "start_at": "2013-06-20T00:00:00Z",
                "title": "Awesome",
                "url": "awesome-event",
                "is_public": "true",
                "tz_offset": -240
            }


+ Response 201 (application/json)
    + Body

            {
                "account": "/partner_v1/account/1/",
                "is_enabled": false,
                "end_at": "2013-06-21T00:00:00Z",
                "locations": [],
                "photo_count": 0,
                "pin": "8092",
                "is_public": true,
                "resource_uri": "/partner_v1/event/1/",
                "start_at": "2013-06-20T00:00:00Z",
                "title": "Awesome",
                "tz_offset": -240,
                "url": "awesome-event"
            }

# Event [/event/{id}/]

+ Parameters
    + id (required, integer, `1`) ... The event id

+ Model (application/json)
    + Body

            {
                "account": "/partner_v1/account/1/",
                "is_enabled": true,
                "end_at": "2013-06-21T00:00:00Z",
                "locations": [
                    {
                        "address": "1 Lucille Lane, Sudden Valley, California, United States",
                        "event": "/partner_v1/event/1/",
                        "lat": "33.640800",
                        "lng": "-117.603100",
                        "resource_uri": "/partner_v1/location/1/"
                    }
                ],
                "photo_count": 41,
                "pin": "1234",
                "is_public": false,
                "resource_uri": "/partner_v1/event/2/",
                "start_at": "2013-06-20T00:00:00Z",
                "title": "Awesome",
                "tz_offset": 0,
                "url": "awesome-event"
            }

## Get Event [GET]
Details about a specific event.

+ Parameters
    + id (required, integer, `1`) ... The event id
    + size = `orig` (optional, string, `crop`) ... Specify the image size to return.
        This parameter is only useful if using `image/jpeg` with the `Accept` header.
        + Values
            + `orig`
            + `crop`
            + `<H>x<W>`

+ Request Metadata
    + Headers

            Accept: application/json

+ Response 200
    [Event][]

+ Request Binary Image Data
    + Headers

            Accept: image/jpeg

+ Response 200 (image/jpeg)
    + Body

            <Binary Image Data>

### Update Event [PATCH]
Update an event. The event url must be unique.

+ Request (application/json)
    + Body

            {
                "account": "/partner_v1/account/1/",
                "end_at": "2013-06-21T00:00:00Z",
                "start_at": "2013-06-20T00:00:00Z",
                "title": "New Awesome Title",
                "url": "my-new-event-url",
                "is_public": "true",
                "tz_offset": "-300"
            }

+ Response 202 (application/json)
    + Body

            {
                "account": "/partner_v1/account/1/",
                "is_enabled": false,
                "end_at": "2013-06-21T00:00:00Z",
                "locations": [],
                "photo_count": 0,
                "pin": "8092",
                "pk": "44",
                "is_public": true,
                "resource_uri": "/partner_v1/event/1/",
                "start_at": "2013-06-20T00:00:00Z",
                "title": "New Awesome Title",
                "tz_offset": -300,
                "url": "my-new-event-url"
            }

# Delete Event [DELETE]
Deletes the specified event and related data (photos, guests, etc.).

+ Response 204

# Group Guests
An *event* typically has many guests. Information about guests is used throught Snapable
to provide context. When a photo is taken, and the guest 
has opted to provide basic information, this information can be displayed with the
photo. An example would be to provide the guest name to give them credit for the
photo.

A guest should only be able to upload photos and should not be able to delete photos
or edit event details.

## Guest List [/guest/]

+ Model (application/json)
    + Body

            {
                "meta": {
                    "limit": 50,
                    "next": null,
                    "offset": 0,
                    "previous": null,
                    "total_count": 3
                },
                "objects": [
                    {
                        "email": "gob@example.com",
                        "event": "/partner_v1/event/1/",
                        "name": "GOB",
                        "resource_uri": "/partner_v1/guest/3/"
                    },
                    {
                        "email": "lindsay@example.com",
                        "event": "/partner_v1/event/1/",
                        "name": "Lindsay Bluth Fünke",
                        "resource_uri": "/partner_v1/guest/4/"
                    },
                    {
                        "email": "buster@example.com",
                        "event": "/partner_v1/event/1/",
                        "name": "Buster Bluth",
                        "resource_uri": "/partner_v1/guest/5/"
                    }
                ]
            }

### Get Guests [GET]

+ Response 200
    [Guest List][]

### Create Guest [POST]

+ Request (application/json)
    + Body

            {
                "event": "/partner_v1/event/1/",
                "email": "gob@example.com",
                "name": "GOB"
            }

+ Response 201 (application/json)
    + Body

            {
                "email": "gob@example.com",
                "event": "/partner_v1/event/1/",
                "name": "GOB",
                "resource_uri": "/partner_v1/guest/3/"
            }

## Guest [/guest/{id}/]

+ Parameters
    + id (required, integer, `1`) ... The guest id

+ Model (application/json)
    + Body

            {
                "email": "gob@example.com",
                "event": "/partner_v1/event/1/",
                "name": "GOB",
                "resource_uri": "/partner_v1/guest/3/"
            }

### Get Guest [GET]

+ Response 200
    [Guest][]

### Update Guest [PATCH]

+ Request (application/json)
    + Body

            {
                "event": "/partner_v1/event/1/",
                "email": "gob@example.com",
                "name": "George Oscar Bluth Jr."
            }

+ Response 202
    [Guest][]

### Delete Guest [DELETE]

+ Response 204

# Group Locations
The event location is optional but highly recommended. It is required for advanced
features such as the "Nearby Events" on the mobile apps. It simply contains a
human readable address and lat/lng coordinate (used by the mobile apps).

# Group Photos
A *photo* resource is the most important resource of the Snapable API and also the
most complex. The photo resource contains both metadata (ie. timestamp, guest that took
the photo, event it belongs to, etc.) as well as the actual photo data.

Photos are currently stored as JPEG. You can request various sizes from the API
with an optional size parameter.

# Group Users
A user belongs to an account and is what is considered the *event organizer*. Users
should be the only ones deleting photos and modifying event details.
