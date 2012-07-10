# first level: independent models
from api.data.models.user import User
from api.data.models.package import Package
from api.data.models.type import Type

# second level: depends on independent models
from api.data.models.event import Event # depends: User, Package
from api.data.models.address import Address # depends: Event
from api.data.models.guest import Guest # depends: Event, Type

# third level: depends on second level models or below
from api.data.models.photo import Photo # depends: Event, Guest, Type
from api.data.models.album import Album # depends: Event, Type

# fourth level: depends on third level models
from api.data.models.albumphoto import AlbumPhoto # depends: Album, Photo