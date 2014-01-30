# python
import mimetypes

# django/tastypie/libs
from django.conf import settings
from PIL import Image
import tastypie.exceptions
import tastypie.http
from tastypie.serializers import Serializer

# snapable
from data.models import Event, Photo
from data.images import SnapImage


class SnapSerializer(Serializer):
    formats = Serializer.formats + [
        'jpeg'
    ]
    content_types = dict(Serializer.content_types, **{
        'jpeg': 'image/jpeg',
    })

    def to_jpeg(self, bundle, options=None):
        size = 'crop'

        if isinstance(bundle.obj, Photo):
            photo = bundle.obj

            # set the size variable
            if ('size' in bundle.request.GET):
                size = bundle.request.GET['size']
            try:
                snapimg = photo.get_image(size)
                return snapimg.img.tobytes('jpeg', 'RGB')
            except Exception as e:
                #photo.delete() # is there really a point to keep metadata for something without a photo
                photo.streamable = False
                photo.save()
                raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        elif isinstance(bundle.obj, Event):
            # set the size variable
            if ('size' in bundle.request.GET):
                size = bundle.request.GET['size']

            # event cover it is set
            if (bundle.obj.cover != None):
                snapimg = bundle.obj.cover.get_image(size)

                if snapimg is None:
                    raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
                else:
                    return snapimg.img.tostring('jpeg', 'RGB')
            # there is no cover and at least one photo
            elif (bundle.obj.cover == None and bundle.obj.photo_count >= 1):
                first_photo = list(Photo.objects.filter(event_id=bundle.obj.pk).order_by('created_at'))[0]
                snapimg = first_photo.get_image(size)

                if snapimg is None:
                    raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
                else:
                    return snapimg.img.tobytes('jpeg', 'RGB')
            # no photo, no cover, return exception
            else:
                raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())
        else:
            return ''

    def from_jpeg(self, content):
        """
        TODO determine if we can parse jpeg
        """
        data = []
        return data

class MultipartSerializer(Serializer):
    """
    The multipart/form-data encoding source code is largely inspired by:
    http://code.activestate.com/recipes/146306/
    """
    boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
    formats = Serializer.formats + [
        'multipart'
    ]
    content_types = dict(Serializer.content_types, **{
        'multipart': 'multipart/form-data; boundary=%s' % boundary,
    })

    @staticmethod
    def encode_multipart_formdata(boundary, fields):
        """
        fields is a dictionary of elements for form fields.
        Return (body)
        """
        CRLF = '\r\n'
        L = []
        for key in fields:
            # if it has a nested dict, assume it's for a file
            if type(fields[key]) == dict:
                filename = fields[key]['filename']
                value = fields[key]['data']
                L.append('--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
                L.append('Content-Type: %s' % MultipartSerializer.get_content_type(filename))
                L.append('')
                L.append(value)
            # otherwise assume it's just a regular key/value pair
            else:
                L.append('--' + boundary)
                L.append('Content-Disposition: form-data; name="%s"' % key)
                L.append('')
                L.append(fields[key])
            
        L.append('--' + boundary + '--')
        L.append('')
        body = CRLF.join(L)
        return body

    @staticmethod
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


    def to_multipart(self, data, options=None):
        body = MultipartSerializer.encode_multipart_formdata(MultipartSerializer.boundary, data)
        return body

    def from_multipart(self, content):
        data = []
        return data