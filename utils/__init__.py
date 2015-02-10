# -*- coding: utf-8 -*-
import re
import sys

from distutils.util import strtobool
from os import environ

# snapable
from .loggers import Log


def env_str(val, default=''):
    """
    Gets a string based environment value or default.
    """
    return environ.get(val, str(default))


def env_bool(val, default=False):
    """
    Gets a string based environment value and returns the Python boolean
    equivalent or default.
    """
    value = environ.get(val, '').lower()
    if len(value) > 0:
        return bool(strtobool(value))
    else:
        return default


def env_int(val, default=0):
    """
    Gets a string based environment value and returns the Python integer
    equivalent or default.
    """
    return int(environ.get(val, default))


def docker_link_protocol(alias_name, default='tcp'):
    """
    Get the protocol from the docker link alias or return the default.
    """
    # ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    # docker_link_host('DB') -> tcp
    try:
        return _split_docker_link(alias_name)[0]
    except Exception:
        return default


def docker_link_host(alias_name, default='127.0.0.1'):
    """
    Get the host from the docker link alias or return the default.
    """
    # ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    # docker_link_host('DB') -> 172.17.0.82
    try:
        return _split_docker_link(alias_name)[1]
    except Exception:
        return default


def docker_link_port(alias_name, default=0):
    """
    Get the port from the docker link alias or return the default.
    """
    # ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    # docker_link_port('DB') -> 5432
    try:
        return int(_split_docker_link(alias_name)[2])
    except Exception:
        return default


def _split_docker_link(alias_name):
    """
    Splits a docker link string into a list of 3 items (protocol, host, port).
    - Assumes IPv4 Docker links (Do IPv6 Docker links even exists?)
    """
    # ex: _split_docker_link_string('DB') -> ['tcp', '172.17.0.82', '8080']
    return filter(None, re.split(r':|//', environ.get('{0}_PORT'.format(alias_name.strip().upper()), '')))


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
