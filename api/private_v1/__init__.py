from tastypie.api import Api

from resources import AddressResource
from resources import AlbumResource
from resources import EventResource
from resources import PhotoResource
from resources import PackageResource
from resources import UserResource

class SnapableApi(Api):

    def __init__(self):
        Api.__init__(self, api_name='private_v1')
        self.register(AddressResource())
        self.register(AlbumResource())
        self.register(EventResource())
        self.register(PhotoResource())
        self.register(PackageResource())
        self.register(UserResource())