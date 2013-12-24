.. _partner_v1-photo:

=====
Photo
=====

A *photo* resource is the most important resource of the Snapable API and also the
most complex. The photo resource contains both metadata (ie. timestamp, guest that took
the photo, event it belongs to, etc.) as well as the actual photo data.

Photos are currently stored as JPEG. You can request various sizes from the API
with an optional size parameter.