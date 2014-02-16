from tastypie.api import Api

import resources

class SnapableApi(Api):

    def __init__(self):
        Api.__init__(self, api_name='private_v1')
        self.register(resources.AccountResource())
        self.register(resources.AccountAddonResource())
        self.register(resources.AccountUserResource())
        self.register(resources.AddonResource())
        self.register(resources.AddressResource())
        self.register(resources.EventResource())
        self.register(resources.EventAddonResource())
        self.register(resources.GuestResource())
        self.register(resources.OrderResource())
        self.register(resources.PhotoResource())
        self.register(resources.PackageResource())
        self.register(resources.UserResource())