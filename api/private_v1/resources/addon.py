# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Addon

class AddonResource(BaseModelResource):

    class Meta(BaseMeta):
        queryset = Addon.objects.all()
        fields = ['title', 'description', 'price', 'enabled']
