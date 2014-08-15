import inspect
import logging
import os
import traceback


class Log:
    """
    A utility class that logs to a predifined logger called 'snapable'.
    """

    @staticmethod
    def d(message, extra=None):
        """Log a debug message."""
        logger = logging.getLogger('snapable')
        logger.debug(message, extra=extra)

    @staticmethod
    def i(message, extra=None):
        """Log an information message."""
        logger = logging.getLogger('snapable')
        logger.info(message, extra=extra)

    @staticmethod
    def w(message, extra=None):
        """Log a warning message."""
        logger = logging.getLogger('snapable')
        logger.warning(message, extra=extra)

    @staticmethod
    def e(message, extra=None):
        """Log an error message."""
        logger = logging.getLogger('snapable')
        logger.error(message, extra=extra)

    @staticmethod
    def c(message, extra=None):
        """Log a critical message."""
        logger = logging.getLogger('snapable')
        logger.critical(message, extra=extra)

    @staticmethod
    def deprecated(message, extra=None, stacklevel=1):
        """
        Log a deprecation warning.
        """
        extra = dict() if extra is None else extra

        # get the frame that called this function, and generate the traceback
        frame = inspect.currentframe() # get the frame
        for i in xrange(1, stacklevel + 1):
            frame = frame.f_back
        co = frame.f_code # the code object
        pathname = os.path.normcase(co.co_filename) # the full path
        func = co.co_name # the function name
        lineno = frame.f_lineno # the line number
        exc_info = None # no exception
        args = None # no args to pass to message (ie. message % args)

        # figure out the trace
        msg = '{0}:{1}: {2}'.format(pathname, lineno, message)
        extra['trace'] = ''.join(traceback.format_stack(frame, 3))

        # log the warning
        logger = logging.getLogger('snapable.deprecated')
        r = logger.makeRecord('snapable.deprecated', logging.WARNING, pathname, lineno, msg, args, exc_info, func=func, extra=extra)
        logger.handle(r)
