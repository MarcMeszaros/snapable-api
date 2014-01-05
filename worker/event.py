# worker import
from __future__ import absolute_import
from worker import app

# python
import os
import shutil
import zipfile

from datetime import datetime, timedelta

# django/tastypie/libs
import pyrax

# snapable
from data.models import Event, Photo

@app.task
def create_images_zip(event_id):
    try:
        # create tempdir and get the event
        tempdir = tempfile.mkdtemp(prefix='snap_api_event_{0}_'.format(event_id))
        event = Event.objects.get(pk=event_id)
        photos = event.photo_set.all()

        # loop through all the photos, and save to disk on the worker server
        for photo in photos:
            photo.img.save('{0}/{1}.jpg'.format(tempdir, photo.pk))

        # create the zip file [PS: awesome new python 2.7+ function! :-) ]
        zip_path = shutil.make_archive(photo.pk, 'zip', event.url)

        # upload the zip to the CDN
        conn = pyrax.connect_to_cloudfiles(public=settings.RACKSPACE_CLOUDFILE_PUBLIC_NETWORK)
        cont = None
        try:
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
        except pyrax.exceptions.NoSuchContainer as e:
            cont = conn.create_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
            conn.make_container_public(cont.name)
            Log.i('created a new CDN container: ' + settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(self.event.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
        
        cont.upload_file(zip_path)

        # delete local zip
        os.remove(zip_path)
    finally:
        # delete temp
        shutil.rmtree(tempdir)
