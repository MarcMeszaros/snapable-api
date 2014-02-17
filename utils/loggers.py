import logging
import sys
import traceback
import warnings

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
        warnings.warn(message, DeprecationWarning, stacklevel=stacklevel+2)

        # get the frame that called this function, and generate the traceback
        frame = sys._getframe(stacklevel-1) # private function, bad practice...
        stack_info = traceback.print_stack(frame) # convert to a text
        extra['traceback'] = stack_info # add the traceback to the log message

        # log the warning
        logger = logging.getLogger('snapable')
        logger.warning(message, extra=extra)
