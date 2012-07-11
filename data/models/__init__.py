# first level: independent models
from data.models.user import User
from data.models.package import Package
from data.models.type import Type

# second level: depends on independent models
from data.models.event import Event # depends: User, Package
from data.models.address import Address # depends: Event
from data.models.guest import Guest # depends: Event, Type

# third level: depends on second level models or below
from data.models.photo import Photo # depends: Event, Guest, Type
from data.models.album import Album # depends: Event, Type

# fourth level: depends on third level models
from data.models.albumphoto import AlbumPhoto # depends: Album, Photo