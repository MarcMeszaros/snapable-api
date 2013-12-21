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
        duration = time() - request.timer # seconds

        # log the response
        logger = logging.getLogger('snapable.request')
        if 'RAW_URI' in request.META:
            url = request.META['RAW_URI']
        else:
            url = request.path

        # log the request
        if 'HTTP_AUTHORIZATION' in request.META and 'HTTP_ACCEPT' in request.META:
            logger.info('{0} {1} [{2}] ({3}) {4}'.format(request.META['REQUEST_METHOD'], response.status_code, duration, request.META['HTTP_ACCEPT'], url))
        else:
            logger.info('{0} {1} {2}'.format(request.META['REQUEST_METHOD'], response.status_code, url))

        return response