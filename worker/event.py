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
    app.backend.set('event:{0}:create_album_zip'.format(event_id), 1)

    event = Event.objects.get(pk=event_id)

    # establish a connection to the CDN
    cont = None
    try:
        cont = rackspace.cloud_files.get_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
    except rackspace.pyrax.exceptions.NoSuchContainer as e:
        cont = rackspace.cloud_files.create_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
        rackspace.cloud_files.make_container_public(cont.name)
        Log.i('created a new CDN container: ' + settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

    # (add try IO error block?)

    # create tempdir and get the photos
    tempdir = tempfile.mkdtemp(prefix='snap_api_event_{0}_'.format(event_id))
    photos = event.photo_set.all()

    # loop through all the photos, and save to disk on the worker server
    for photo in photos:
        photo.get_image().img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))

    # create and upload the zip file
    zip_path = shutil.make_archive(tempfile.tempdir+"/"+str(event.uuid),'zip', tempdir)
    zip_obj = cont.upload_file(zip_path)

    # cleanup
    os.remove(zip_path)
    shutil.rmtree(tempdir)

    zip_cdn_url = cont.cdn_uri + "/" + str(event.uuid) + ".zip"

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
