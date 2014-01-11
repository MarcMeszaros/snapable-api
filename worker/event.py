# worker import
from __future__ import absolute_import
from worker import app

# python
import os
import shutil
import zipfile
import tempfile

# django/tastypie/libs
import pyrax

from django.conf import settings
from django.template import Context
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

# snapable
import settings

from data.models import Event, Photo, AccountUser
from api.utils.loggers import Log

@app.task
def create_album_zip(event_id):

    # add lock
    app.backend.set('create_album_zip_'+event_id, 'RUNNING')

    event = Event.objects.get(pk=event_id)

    # establish a connection to the CDN
    conn = pyrax.connect_to_cloudfiles(public=settings.RACKSPACE_CLOUDFILE_PUBLIC_NETWORK)
    cont = None
    try:
        cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
    except pyrax.exceptions.NoSuchContainer as e:
        cont = conn.create_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
        conn.make_container_public(cont.name)
        Log.i('created a new CDN container: ' + settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

    # (add try IO error block?)

    # create tempdir and get the photos
    tempdir = tempfile.mkdtemp(prefix='snap_api_event_{0}_'.format(event_id))
    photos = event.photo_set.all()

    # loop through all the photos, and save to disk on the worker server
    for photo in photos:
        photo.get_image().img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))

    # create and upload the zip file
    zip_path = shutil.make_archive(tempfile.tempdir+"/"+event.title,'zip', tempdir)
    zip_obj = cont.upload_file(zip_path)

    # cleanup
    os.remove(zip_path)
    shutil.rmtree(tempdir)

    # issue temp URL (24h = 86400 seconds)
    zip_temp_url = zip_obj.get_temp_url(86400)

    # mail zip url

    # load in the templates
    plaintext = get_template('zip_url.txt')
    html = get_template('zip_url.html')

    # setup the template context variables
    d = Context({ 'zip_temp_url': zip_temp_url })

    # build the email
    email = AccountUser.objects.get(account_id=event.account_id).user.email
    subject, from_email, to = 'Your Snapable album is ready for download', 'support@snapable.com', [email]
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    #if settings.DEBUG == False:
    msg.send()

    # remove lock
    app.backend.delete('create_album_zip_'+event_id)
