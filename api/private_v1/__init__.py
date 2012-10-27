from tastypie.api import Api

from resources import AccountResource
from resources import AccountAddonResource
from resources import AddonResource
from resources import AddressResource
from resources import AlbumResource
from resources import EventResource
from resources import EventAddonResource
from resources import GuestResource
from resources import OrderResource
from resources import PhotoResource
from resources import PackageResource
from resources import TypeResource
from resources import UserResource

class SnapableApi(Api):

    def __init__(self):
        Api.__init__(self, api_name='private_v1')
        self.register(AccountResource())
        self.register(AccountAddonResource())
        self.register(AddonResource())
        self.register(AddressResource())
        #self.register(AlbumResource())
        self.register(EventResource())
        self.register(EventAddonResource())
        self.register(GuestResource())
        self.register(OrderResource())
        self.register(PhotoResource())
        self.register(PackageResource())
        self.register(TypeResource())
        self.register(UserResource())