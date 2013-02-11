# first level: independent models
from api.models.account import ApiAccount

# second level: depends on independent models
from api.models.key import ApiKey # depends: ApiAccount