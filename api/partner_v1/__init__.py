from tastypie.api import Api

import resources

class SnapableApi(Api):

    def __init__(self):
        Api.__init__(self, api_name='partner_v1')
        self.register(resources.AccountResource())
        self.register(resources.EventResource())
        self.register(resources.UserResource())