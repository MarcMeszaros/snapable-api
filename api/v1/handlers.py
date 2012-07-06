from piston.handler import BaseHandler
from piston.utils import rc, throttle

class ApiHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, data=None ):

        if (data != None):
            return { 'data': data, 'data_length': len(data) }
        else:
            return { 'data': '', 'data_length': 0 }