import api.auth
import api.v1.resources
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest

class UserResource(api.v1.resources.UserResource):

    Meta = api.v1.resources.UserResource.Meta # set Meta to the public API Meta
    Meta.fields += ['billing_zip', 'terms']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.UserResource.__init__(self)

    def dehydrate(self, bundle):
        db_pass = bundle.obj.password.split('$')

        if len(db_pass) >= 3:
            bundle.data['password_algorithm'] = db_pass[0]
            bundle.data['password_iterations'] = db_pass[1]
            bundle.data['password_salt'] = db_pass[2]

        return bundle

    def hydrate(self, bundle):

        if 'password' in bundle.data.keys():
            bundle.obj.set_password(bundle.data['password'])
        else:
            try:
                password = []
                password.append(bundle.data['password_algorithm'])
                password.append(bundle.data['password_iterations'])
                password.append(bundle.data['password_salt'])
                password.append(bundle.data['password_hash'])

                bundle.obj.password = "$".join(password)
            except KeyError as key:
                raise BadRequest('Missing field: ' + str(key))

        return bundle