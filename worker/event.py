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
import settings

from data.models import Event, Photo, AccountUser
from utils import rackspace

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
    photos = event.photo_set.all().values_list('pk', flat=True)

    # loop through all the photo ids, and save to disk on the worker server
    for photo_id in photos:
        try:
            photo = Photo.objects.get(pk=photo_id)
            photo.get_image().img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))
        except AttributeError as e:
            Log.e('missing attribute')

    # create and upload the zip file
    zip_path = shutil.make_archive('{0}/{1}'.format(tempfile.tempdir, event.uuid), 'zip', tempdir)
    zip_obj = cont.upload_file(zip_path)

    # cleanup
    os.remove(zip_path)
    shutil.rmtree(tempdir)

    zip_cdn_url = '{0}/{1}.zip'.format(cont.cdn_uri, event.uuid)

    # mail zip url

    # load in the templates
    plaintext = get_template('zip_url.txt')
    html = get_template('zip_url.html')

    # setup the template context variables
    d = Context({ 'zip_url': zip_cdn_url })

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
