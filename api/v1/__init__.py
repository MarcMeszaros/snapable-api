from tastypie.api import Api

from resources import AlbumResource
from resources import EventResource
from resources import PhotoResource
from resources import UserResource

class SnapableApi(Api):

    def __init__(self):
        Api.__init__(self, api_name='1')
        self.register(AlbumResource())
        self.register(EventResource())
        self.register(PhotoResource())
        self.register(UserResource())