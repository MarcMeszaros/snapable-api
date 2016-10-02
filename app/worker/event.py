# worker import
from __future__ import absolute_import
from worker import app

# python
import os
import shutil
import zipfile
import tempfile

# django/tastypie/libs
import unicodecsv as csv
from django.conf import settings
from django.template import Context
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from uuidfield import UUIDField

# snapable
from data.models import AccountUser, Event, Guest, Photo
from utils import rackspace, redis
from utils.loggers import Log


from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@app.task
def cleanup_photos(event_id):
    event = Event.objects.get(pk=event_id)
    photos = event.photo_set.all()

    for photo in photos:
        photo.cleanup_resizes()


@app.task
def update_redis_zip_counts():
    events = Event.objects.all()
    for event in events:
        try:
            redis.client.setex('event:{0}:zip_photo_count'.format(event.id), 3600, event.zip_photo_count)
        except:
            pass


@app.task
def create_album_zip(event_id, send_email=True):

    # add lock
    app.backend.client.setex('event:{0}:create_album_zip'.format(event_id), 1, 900) # expire in 15 mins

    event = Event.objects.get(pk=event_id)

    # establish a connection to the CDN
    cont = None
    cont_name = '{0}{1}'.format(settings.CLOUDFILES_DOWNLOAD_PREFIX, (event.pk / settings.CLOUDFILES_EVENTS_PER_CONTAINER))
    try:
        cont = rackspace.cloud_files.get_container(cont_name)
    except rackspace.pyrax.exceptions.NoSuchContainer as e:
        cont = rackspace.cloud_files.create_container(cont_name)
        rackspace.cloud_files.make_container_public(cont.name)
        Log.i('created a new CDN container: {0}'.format(cont.name))

    # (add try IO error block?)

    # create tempdir and get the photos
    tempdir = tempfile.mkdtemp(prefix='snap_api_event_{0}_'.format(event_id))
    photos = list(event.photo_set.filter(is_archived=False).values_list('pk', flat=True))

    # loop through all the photo ids, and save to disk on the worker server
    captions = dict()
    for photo_id in photos:
        try:
            photo = Photo.objects.get(pk=photo_id)
            image = photo.get_image()
            if image:
                image.img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))
                captions['{}.jpg'.format(photo.pk)] = photo.caption
        except AttributeError as e:
            Log.w('Missing attribute on photo object')

    # create the csv file
    with open('{}/captions.csv'.format(tempdir), 'w') as csvfile:
        fieldnames = ['filename', 'caption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for k, v in captions.items():
            writer.writerow({'filename': k, 'caption': v})

    # create and upload the zip file
    zip_path = shutil.make_archive('{0}/{1}'.format(tempfile.tempdir, event.uuid), 'zip', tempdir)
    zip_obj = cont.upload_file(zip_path)
    # set metadata
    with zipfile.ZipFile(zip_path) as zip_file:
        # exclude './' and 'captions.csv' from count
        file_count = len(zip_file.namelist()) - 2
        metadata = {'X-Object-Meta-Photos': str(file_count)}
        zip_obj.set_metadata(metadata, clear=True)
        redis.client.setex('event:{0}:zip_photo_count'.format(event_id), 1800, file_count)

    # cleanup
    os.remove(zip_path)
    shutil.rmtree(tempdir)

    # TODO remove this 'if' hack once pyrax starts behaving
    # & cont.cdn_uri isn't None
    cdn_uri = cont.cdn_uri
    if cdn_uri is None:
        if 'dev' in settings.CLOUDFILES_DOWNLOAD_PREFIX:
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

    if send_email:
        msg.send()

    # remove (expire) lock
    app.backend.expire('event:{0}:create_album_zip'.format(event_id), 30)


@app.task
def goodbye_album_zip(event_id, send_email=True):

    event = Event.objects.get(pk=event_id)

    # load in the templates
    plaintext = get_template('goodbye_zip_url.txt')
    html = get_template('goodbye_zip_url.html')

    # setup the template context variables
    d = Context({'zip_url':  event.zip_download_url})

    # build the email
    email = AccountUser.objects.get(account_id=event.account_id).user.email
    subject, from_email, to = 'Goodbye - final Snapable album download', 'support@snapable.com', [email]
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    if event.photo_count > 0 and send_email:
        msg.send()


@app.task
def email_guests(event_id, message=''):
    event = Event.objects.get(pk=event_id)
    guests = event.guest_set.filter(is_invited=False)

    for guest in guests:
        guest.send_email(message)
