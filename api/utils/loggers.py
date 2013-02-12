import logging

class Log:
    """
    A utility class that logs to a predifined logger called 'snapable'.
    """

    @staticmethod
    def d(message):
        """Log a debug message."""
        logger = logging.getLogger('snapable')
        logger.debug(message)

    @staticmethod
    def i(message):
        """Log a information message."""
        logger = logging.getLogger('snapable')
        logger.info(message)

    @staticmethod
    def w(message):
        """Log a warning message."""
        logger = logging.getLogger('snapable')
        logger.warning(message)

    @staticmethod
    def e(message):
        """Log a error message."""
        logger = logging.getLogger('snapable')
        logger.error(message)

    @staticmethod
    def c(message):
        """Log a critical message."""
        logger = logging.getLogger('snapable')
        logger.critical(message)
