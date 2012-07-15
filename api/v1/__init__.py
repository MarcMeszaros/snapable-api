from tastypie.api import Api

from resources.user import UserResource

class SnapableApi(Api):

    def __init__(self, api_name=None):
        Api.__init__(self, api_name='1')
        self.register(UserResource())