import cloudfiles
import StringIO
import tastypie.exceptions
import tastypie.http

import api.loggers

from django.conf import settings
from tastypie.serializers import Serializer

from PIL import Image

class SnapableSerializer(Serializer):
    formats = ['json', 'jpeg']
    content_types = {
        'json': 'application/json',
        'jpeg': 'image/jpeg',
    }

    def to_jpeg(self, bundle, options=None):
        photo = bundle.obj
        event = bundle.obj.event
        size = 'orig'

        # set the size variable
        if (options != None and options.has_key('size')):
            size = options['size']

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
                
                # get the size param
                sizeList = size.split('x')
                sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                out = img.resize(sizeTupple)

                # create the new photo size and save it
                obj = cont.create_object(str(event.id) + '/' + str(photo.id) + '_' + size + '.jpg')
                obj.content_type = 'image/jpeg'
                obj.write(out.tostring('jpeg', 'RGB'))

                return out.tostring('jpeg', 'RGB')
        except cloudfiles.errors.NoSuchObject as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        except cloudfiles.errors.NoSuchContainer as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())

    def from_jpeg(self, content):
        data = []
        return data