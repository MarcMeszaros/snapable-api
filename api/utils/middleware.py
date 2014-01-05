# python
import logging
from time import time

class RequestLoggingMiddleware(object):
    """
    A middleware class that logs all the requests and includes some of the request details.
    """

    def process_request(self, request):
        request.timer = time()
        return None

    def process_response(self, request, response):
        try:
            duration = (time() - request.timer) * 1000 # milliseconds

            # log the response
            logger = logging.getLogger('snapable.request')

            # log the request
            logger.info('{0} {1} [{2}] ({3}) {4}'.format(request.method, response.status_code, duration, request.META['HTTP_ACCEPT'], request.path))
        except Exception:
            pass # if anything goes wrong, just keep going

        return response