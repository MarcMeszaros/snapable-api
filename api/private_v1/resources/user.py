import api.auth
import api.v1.resources

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie import http

from data.models import User

class UserResource(api.v1.resources.UserResource):

    Meta = api.v1.resources.UserResource.Meta # set Meta to the public API Meta
    Meta.fields += ['billing_zip', 'terms']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = api.auth.ServerAuthorization()

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
        elif (
                'password_algorithm' in bundle.data.keys() or 
                'password_iterations' in bundle.data.keys() or 
                'password_salt' in bundle.data.keys() or 
                'password_hash' in bundle.data.keys()
            ):
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

    # should use prepend_url, but doesn't work...
    # seems related to this bug: https://github.com/toastdriven/django-tastypie/issues/584
    def override_urls(self):
        """
        Using override_url
        """
        return [
            url(r'^(?P<resource_name>%s)/auth/$' % self._meta.resource_name, self.wrap_view('dispatch_auth'), name="api_dispatch_auth"),
        ]

    def dispatch_auth(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        try:
            # get the header data
            x_snap_user = request.META['HTTP_X_SNAP_USER']
            user_details = x_snap_user.strip().split(':')

            # put the email in the kwargs for the dispatch call at the end
            kwargs['email'] = user_details[0]

            # get the user model matching the email
            user = User.objects.get(email=user_details[0])

            # get the matched user's password data
            db_pass = user.password.split('$', 1)
            pass_data = {}

            # various data based on db_pass type
            if db_pass[0] == 'bcrypt':
                pass_data['password_algorithm'] = db_pass[0]
                pass_data['password_data'] = db_pass[1]

            elif db_pass[0] == 'pbkdf2_sha256':
                pass_parts = db_pass[1].split('$')

                pass_data['password_algorithm'] = db_pass[0]
                pass_data['password_iterations'] = pass_parts[0]
                pass_data['password_salt'] = pass_parts[1]
                pass_data['password_hash'] = pass_parts[2]

            # if the db password hash and the one in the header match, display the user details
            if pass_data['password_hash'] == user_details[1]:
                return self.dispatch('detail', request, **kwargs)
            else:
                raise BadRequest('Invalid email/password hash combination in header x-SNAP-User')

        except KeyError as key:
            raise BadRequest('Missing field: ' + str(key))
        except ObjectDoesNotExist:
            raise BadRequest('Invalid email/password hash combination in header x-SNAP-User')