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
        db_pass = bundle.obj.password.split('$', 1)

        # various data based on db_pass type 
        if db_pass[0] == 'bcrypt':
            bundle.data['password_algorithm'] = db_pass[0]
            bundle.data['password_data'] = db_pass[1]
        
        elif db_pass[0] == 'pbkdf2_sha256':
            pass_parts = db_pass[1].split('$')

            bundle.data['password_algorithm'] = db_pass[0]
            bundle.data['password_iterations'] = pass_parts[0]
            bundle.data['password_salt'] = pass_parts[1]

        return bundle

    def hydrate(self, bundle):

        if 'password' in bundle.data.keys():
            bundle.obj.set_password(bundle.data['password'])
        else:
            try:
                password = []
                password.append(bundle.data['password_algorithm'])
                
                # if bundle.data['password_algorithm'] == 'bcrypt':
                #    password.append(bundle.data['password_data'])

                if bundle.data['password_algorithm'] == 'pbkdf2_sha256':
                    password.append(bundle.data['password_iterations'])
                    password.append(bundle.data['password_salt'])
                    password.append(bundle.data['password_hash'])

                else:
                    raise BadRequest('Unsupported password hashing algorithm: ' + bundle.data['password_algorithm'])
                    
                bundle.obj.password = "$".join(password)
            except KeyError as key:
                raise BadRequest('Missing field: ' + str(key))

        return bundle