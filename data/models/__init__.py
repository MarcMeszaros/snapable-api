# first level: independent models
from data.models.user import User
from data.models.package import Package
from data.models.type import Type
from data.models.addon import Addon

# second level: depends on independent models
from data.models.account import Account # depends: User
from data.models.passwordnonce import PasswordNonce # depends: User

# third level: depends on second level models or below
#from data.models.accountuser import AccountUser # depends: Account, User
from data.models.event import Event # depends: Account, Package

# fourth level: depends on third level models or below
from data.models.address import Address # depends: Event
from data.models.guest import Guest # depends: Event, Type
from data.models.photo import Photo # depends: Event, Guest, Type
from data.models.order import Order # depends: Account

# fifth level: depends on fourth level models or below
from data.models.album import Album # depends: Event, Type, Photo
from data.models.accountaddon import AccountAddon # depends: Account, Addon
from data.models.eventaddon import EventAddon # depends: Event, Addon

# sixth level: depends on fifth level models or below
from data.models.albumphoto import AlbumPhoto # depends: Album, Photo