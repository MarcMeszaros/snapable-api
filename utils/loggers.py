import logging
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
        warnings.warn(message, DeprecationWarning, stacklevel=stacklevel+2)
        logger = logging.getLogger('snapable')
        logger.warning(message, extra=extra)
