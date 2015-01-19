import os
import sys

# snapable
from .loggers import Log


def str_env(val, default=''):
    """Returns string based environment values"""
    return os.environ.get(val, str(default))


def bool_env(val, default=False):
    """Replaces string based environment values with Python booleans"""
    value = os.environ.get(val, '').lower()
    if len(value) > 0:
        return True if value[0] in ['t', 'y', '1'] else False
    else:
        return default


def int_env(val, default=0):
    """Replaces string based environment values with Python integer"""
    return int(os.environ.get(val, default))


def docker_link_host(alias_name, default=''):
    """Get the host from the docker link alias"""
    try:
        split = os.environ.get('{0}_PORT'.format(alias_name), default).split('//')[1].split(':')
        if len(split) == 2:
            return split[0]
        else:
            return default
    except Exception:
        return default


def docker_link_port(alias_name, default=0):
    """Get the posrt from the docker link alias"""
    try:
        split = os.environ.get('{0}_PORT'.format(alias_name), default).split('//')[1].split(':')
        if len(split) == 2:
            return int(split[1])
        else:
            return default
    except Exception:
        return default


class Dotable(dict):

    __getattr__ = dict.__getitem__

    def __init__(self, d):
        if sys.version_info[:1] == (3,):
            self.update(**dict((k, self.parse(v)) for k, v in d.items()))  # in py3 use .items
        else:
            self.update(**dict((k, self.parse(v)) for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v
