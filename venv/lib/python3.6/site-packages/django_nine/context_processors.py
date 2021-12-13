from django_nine import versions as nine_versions

__title__ = 'django_nine.versions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = [
    'versions',
]


def versions(request):
    """Get active theme.

    :param django.http.HttpRequest request:
    :return dict:
    """
    return {'VERSIONS': nine_versions}
