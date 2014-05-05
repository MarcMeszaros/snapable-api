# django/tastypie/libs
from tastypie.resources import ModelResource, Resource

# snapable
import api.auth
from api.utils.serializers import SnapSerializer

# defaults for this api version
class BaseMeta(object):
    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']
    always_return_data = True
    authentication = api.auth.ServerAuthentication()
    authorization = api.auth.ServerAuthorization()
    serializer = SnapSerializer(formats=['json', 'jpeg'])

class BaseResource(Resource):

    # based on https://github.com/toastdriven/django-tastypie/blob/master/tastypie/resources.py#L1254
    def build_get_list(self, request, resource, objects, **kwargs):
        base_bundle = self.build_bundle(request=request)

        # create the default resource_uri or override
        resource_uri = self.get_resource_uri()
        if 'resource_uri' in kwargs:
            resource_uri = kwargs['resource_uri']

        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=resource_uri, limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []
        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(resource.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return to_be_serialized

    # based on https://github.com/toastdriven/django-tastypie/blob/master/tastypie/resources.py#L1283
    def build_get_detail(self, request, resource, object, **kwargs):
        print('detail')

class BaseModelResource(BaseResource, ModelResource):
    pass