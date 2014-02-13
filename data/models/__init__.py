# modules to import for 'import *'
#__all__ = ['']

#===== Old Imports (Backwards Compatibility) =====#
# first level: independent models
from data.models.account import Account
from data.models.accountaddon import AccountAddon
from data.models.accountuser import AccountUser
from data.models.addon import Addon
from data.models.album import Album
from data.models.albumphoto import AlbumPhoto
from data.models.eventaddon import EventAddon
from data.models.guest import Guest
from data.models.location import Location
from data.models.order import Order
from data.models.package import Package
from data.models.passwordnonce import PasswordNonce
from data.models.user import User

# second level: depends on independent models
from data.models.photo import Photo # depends: Guest

# third level: depends on second level models or below
from data.models.event import Event # depends: Photo