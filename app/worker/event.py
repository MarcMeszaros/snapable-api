# worker import
from __future__ import absolute_import
from worker import app

# python
import os
import shutil
import zipfile
import tempfile

# django/tastypie/libs
from django.conf import settings
from django.template import Context
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from uuidfield import UUIDField

# snapable
from data.models import AccountUser, Event, Guest, Photo
from utils import rackspace
from utils.loggers import Log


@app.task
def cleanup_photos(event_id):
    event = Event.objects.get(pk=event_id)
    photos = event.photo_set.all()

    for photo in photos:
        photo.cleanup_resizes()


@app.task
def create_album_zip(event_id):

    # add lock
    app.backend.client.setex('event:{0}:create_album_zip'.format(event_id), 1, 900) # expire in 15 mins

    event = Event.objects.get(pk=event_id)

    # establish a connection to the CDN
    cont = None
    cont_name = '{0}{1}'.format(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX, (event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
    try:
        cont = rackspace.cloud_files.get_container(cont_name)
    except rackspace.pyrax.exceptions.NoSuchContainer as e:
        cont = rackspace.cloud_files.create_container(cont_name)
        rackspace.cloud_files.make_container_public(cont.name)
        Log.i('created a new CDN container: {0}'.format(cont.name))

    # (add try IO error block?)

    # create tempdir and get the photos
    tempdir = tempfile.mkdtemp(prefix='snap_api_event_{0}_'.format(event_id))
    photos = list(event.photo_set.all().values_list('pk', flat=True))

    # loop through all the photo ids, and save to disk on the worker server
    for photo_id in photos:
        try:
            photo = Photo.objects.get(pk=photo_id)
            photo.get_image().img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))
        except AttributeError as e:
            Log.w('Missing attribute on photo object')

    # create and upload the zip file
    zip_path = shutil.make_archive('{0}/{1}'.format(tempfile.tempdir, event.uuid), 'zip', tempdir)
    zip_obj = cont.upload_file(zip_path)

    # cleanup
    os.remove(zip_path)
    shutil.rmtree(tempdir)

    # TODO remove this 'if' hack once pyrax starts behaving
    # & cont.cdn_uri isn't None
    cdn_uri = cont.cdn_uri
    if cdn_uri is None:
        if 'dev' in settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX:
            cdn_uri = 'http://23e8b3af054c2e288358-8328cee55d412b3e5ad38ec5882590af.r11.cf1.rackcdn.com'
        else:
            cdn_uri = 'http://75e4c45674cfdf4884a0-6f5bbb6cfffb706c990262906f266b0c.r28.cf1.rackcdn.com'
    # mail zip url
    zip_cdn_url = '{0}/{1}.zip'.format(cdn_uri, event.uuid)

    # load in the templates
    plaintext = get_template('zip_url.txt')
    html = get_template('zip_url.html')

    # setup the template context variables
    d = Context({'zip_url': zip_cdn_url})

    # build the email
    email = AccountUser.objects.get(account_id=event.account_id).user.email
    subject, from_email, to = 'Your Snapable album is ready for download', 'support@snapable.com', [email]
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    #if settings.DEBUG == False:
    msg.send()

    # remove (expire) lock
    app.backend.expire('event:{0}:create_album_zip'.format(event_id), 30)


@app.task
def email_guests(event_id, message=''):
    event = Event.objects.get(pk=event_id)
    guests = event.guest_set.filter(is_invited=False)

    for guest in guests:
        guest.send_email(message)
