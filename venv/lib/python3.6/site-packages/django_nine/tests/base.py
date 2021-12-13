import logging

__title__ = 'django_nine.tests.base'
__author__ = 'Artur Barseghyan'
__copyright__ = '2015-2019 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'LOG_INFO',
    'log_info',
)


logger = logging.getLogger(__name__)

LOG_INFO = True


def log_info(func):
    """Logs some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        logger.info('\n\n%s' % func.__name__)
        logger.info('============================')
        if func.__doc__:
            logger.info('""" %s """' % func.__doc__.strip())
        logger.info('----------------------------')
        if result is not None:
            logger.info(result)
        logger.info('\n++++++++++++++++++++++++++++')

        return result
    return inner
