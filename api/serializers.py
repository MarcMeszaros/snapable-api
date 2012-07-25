import cloudfiles
import tastypie.exceptions
import tastypie.http

from django.conf import settings
from tastypie.serializers import Serializer

class SnapableSerializer(Serializer):
    formats = ['json', 'jpeg']
    content_types = {
        'json': 'application/json',
        'jpeg': 'image/jpeg',
    }

    def to_jpeg(self, bundle, options=None):
        photo = bundle.obj
        event = bundle.obj.event

        #connect to container
        try:
            conn = cloudfiles.Connection(settings.RACKSPACE_USERNAME, settings.RACKSPACE_APIKEY, 10)
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(event.id / 1000))
            obj = cont.get_object(str(event.id) + '/' + str(photo.id) + '_orig.jpg')
            return obj.read()
        except cloudfiles.errors.NoSuchObject as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        except cloudfiles.errors.NoSuchContainer as e:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())

    def from_jpeg(self, content):
        data = []
        return data