import api.auth
import api.v1.resources
import re

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.utils import dict_strip_unicode_keys
from tastypie import http

from data.models import PasswordNonce
from data.models import User

class UserResource(api.v1.resources.UserResource):

    Meta = api.v1.resources.UserResource.Meta # set Meta to the public API Meta
    Meta.fields += ['billing_zip', 'terms']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.passwordreset_allowed_methods = ['get', 'post']
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

    # should use prepend_url, but only works with tastypie v0.9.12+
    # seems related to this bug: https://github.com/toastdriven/django-tastypie/issues/584
    def override_urls(self):
        """
        Using override_url
        """
        return [
            url(r'^(?P<resource_name>%s)/auth/$' % self._meta.resource_name, self.wrap_view('dispatch_auth'), name="api_dispatch_auth"),
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/passwordreset/$' % self._meta.resource_name, self.wrap_view('dispatch_passwordreset'), name="api_dispatch_passwordreset"),
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

    def dispatch_passwordreset(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        return self.dispatch('passwordreset', request, **kwargs)

    def post_passwordreset(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        location = self.get_resource_uri(bundle)

        # get the user
        user = User.objects.get(pk=kwargs['pk'])

        # create the passwordnonce and save
        passnonce = PasswordNonce()
        passnonce.user = user
        passnonce.valid = True
        passnonce.save()

        # whitelist check for url
        if ('url' in bundle.data.keys() and re.match('https?://(.+\.)?snapable\.com', bundle.data['url']) != None):
            # load in the templates
            plaintext = get_template('passwordreset_email.txt')
            html = get_template('passwordreset_email.html')

            # setup the template context variables
            resetUrl = bundle.data['url']+passnonce.nonce
            d = Context({'reset_url': resetUrl })

            # build the email
            subject, from_email, to = 'Snapable: Password Reset', 'team@snapable.com', [user.email]
            text_content = plaintext.render(d)
            html_content = html.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        elif ('url' in bundle.data.keys()):
            raise BadRequest('Invalid URL. Must be of type http(s)://*.snapable.com')

        return http.HttpCreated(location=location)

    def get_passwordreset(self, request, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])

        objects = PasswordNonce.objects.filter(user=user.id, valid=True)
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.build_bundle(obj=obj) for obj in sorted_objects]

        nonces = []
        for bundle in bundles:
            nonces += [{
                'nonce': bundle.obj.nonce,
                'timestamp': bundle.obj.timestamp,
            }]

        to_be_serialized['objects'] = nonces

        #to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        return self.create_response(request, to_be_serialized)