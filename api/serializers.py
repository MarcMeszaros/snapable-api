import cloudfiles
import StringIO
import tastypie.exceptions
import tastypie.http

import api.loggers

from django.conf import settings
from tastypie.serializers import Serializer

from data.models import Photo
from data.images import SnapImage

from PIL import Image

class PhotoSerializer(Serializer):
    formats = Serializer.formats + [
        'jpeg'
    ]
    content_types = dict(Serializer.content_types, **{
        'jpeg': 'image/jpeg',
    })

    def to_jpeg(self, bundle, options=None):
        photo = bundle.obj
        event = bundle.obj.event
        size = 'orig'

        # set the size variable
        if (bundle.data != None and bundle.data.has_key('size')):
            size = bundle.data['size']

        #connect to container
        try:
            conn = cloudfiles.Connection(settings.RACKSPACE_USERNAME, settings.RACKSPACE_APIKEY, settings.RACKSPACE_CLOUDFILE_TIMEOUT)
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(event.id / 1000))

            # try an get the size wanted
            try:
                obj = cont.get_object(str(event.id) + '/' + str(photo.id) + '_' + size + '.jpg')
                return obj.read()
            except:
                # get the original size photo and create a Image object based on it
                obj_orig = cont.get_object(str(event.id) + '/' + str(photo.id) + '_orig.jpg')
                data = obj_orig.read()
                img = Image.open(StringIO.StringIO(data))
                snapimg = SnapImage(img)
                
                # get the size param and resize
                sizeList = size.split('x')
                sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                snapimg.resize(sizeTupple)

                # save the new photo size
                obj = cont.create_object(str(event.id) + '/' + str(photo.id) + '_' + size + '.jpg')
                obj.content_type = 'image/jpeg'
                obj.write(snapimg.img.tostring('jpeg', 'RGB'))

                return snapimg.img.tostring('jpeg', 'RGB')
        except cloudfiles.errors.NoSuchObject as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        except cloudfiles.errors.NoSuchContainer as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())

    def from_jpeg(self, content):
        data = []
        return data

class EventSerializer(Serializer):
    formats = Serializer.formats + [
        'jpeg'
    ]
    content_types = dict(Serializer.content_types, **{
        'jpeg': 'image/jpeg',
    })

    def to_jpeg(self, bundle, options=None):
        event = bundle.obj
        size = 'orig'

        # get the photo count
        photos_count = Photo.objects.filter(event_id=event.id).count()

        # set the size variable
        if (bundle.data != None and bundle.data.has_key('size')):
            size = bundle.data['size']

        #connect to container
        try:
            conn = cloudfiles.Connection(settings.RACKSPACE_USERNAME, settings.RACKSPACE_APIKEY, settings.RACKSPACE_CLOUDFILE_TIMEOUT)
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(event.id / 1000))


            # event cover it is set
            if (event.cover != 0):
                cover_photo = Photo.objects.get(pk=event.cover)
                try:
                    obj = cont.get_object(str(cover_photo.event.id) + '/' + str(cover_photo.id) + '_' + size + '.jpg')
                    return obj.read()
                except:
                    # get the original size photo and create a Image object based on it
                    obj_orig = cont.get_object(str(cover_photo.event.id) + '/' + str(cover_photo.id) + '_orig.jpg')
                    data = obj_orig.read()
                    img = Image.open(StringIO.StringIO(data))
                    snapimg = SnapImage(img)
                    
                    # get the size param and resize
                    sizeList = size.split('x')
                    sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                    snapimg.resize(sizeTupple)

                    # save the new photo size
                    obj = cont.create_object(str(cover_photo.event.id) + '/' + str(cover_photo.id) + '_' + size + '.jpg')
                    obj.content_type = 'image/jpeg'
                    obj.write(snapimg.img.tostring('jpeg', 'RGB'))

                    return snapimg.img.tostring('jpeg', 'RGB')
            # there is no cover and at least one photo
            elif (event.cover == 0 and photos_count >= 1):
                first_photo = list(Photo.objects.filter(event_id=event.id).order_by('timestamp'))[0]
                try:
                    obj = cont.get_object(str(first_photo.event.id) + '/' + str(first_photo.id) + '_' + size + '.jpg')
                    return obj.read()
                except:
                    # get the original size photo and create a Image object based on it
                    obj_orig = cont.get_object(str(first_photo.event.id) + '/' + str(first_photo.id) + '_orig.jpg')
                    data = obj_orig.read()
                    img = Image.open(StringIO.StringIO(data))
                    snapimg = SnapImage(img)
                    
                    # get the size param and resize
                    sizeList = size.split('x')
                    sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                    snapimg.resize(sizeTupple)

                    # save the new photo size
                    obj = cont.create_object(str(first_photo.event.id) + '/' + str(first_photo.id) + '_' + size + '.jpg')
                    obj.content_type = 'image/jpeg'
                    obj.write(snapimg.img.tostring('jpeg', 'RGB'))

                    return snapimg.img.tostring('jpeg', 'RGB')
            # no photo, no cover, return exception
            else:
                raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        except cloudfiles.errors.NoSuchObject as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        except cloudfiles.errors.NoSuchContainer as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())

    def from_jpeg(self, content):
        data = []
        return data