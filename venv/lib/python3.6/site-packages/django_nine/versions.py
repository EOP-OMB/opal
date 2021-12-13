"""
Contains information about the current Django version in use, including (LTE
and GTE).
"""

from distutils.version import LooseVersion

import django

__title__ = 'django_nine.versions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = [
    'LOOSE_DJANGO_VERSION', 'LOOSE_DJANGO_MINOR_VERSION',
]

LOOSE_DJANGO_VERSION = LooseVersion(django.get_version())
LOOSE_DJANGO_MINOR_VERSION = LooseVersion(
    '.'.join([str(i) for i in LOOSE_DJANGO_VERSION.version[0:2]])
)

# Loose versions
LOOSE_VERSIONS = (
    '1.4',
    '1.5',
    '1.6',
    '1.7',
    '1.8',
    '1.9',
    '1.10',
    '1.11',
    '2.0',
    '2.1',
    '2.2',
    '3.0',
    '3.1',
    '3.2',
    '4.0',
    '4.1',
    '4.2',
    '5.0',
    '5.1',
    '5.2',
    '6.0',
    '6.1',
    '6.2',
)

for v in LOOSE_VERSIONS:
    var_name = 'LOOSE_VERSION_{0}'.format(v.replace('.', '_'))
    globals()[var_name] = LooseVersion(v)
    __all__.append(var_name)

# Exact versions
EXACT_VERSIONS = LOOSE_VERSIONS[:-1]

for i, v in enumerate(EXACT_VERSIONS):
    l_cur = globals()['LOOSE_VERSION_{0}'
                      ''.format(LOOSE_VERSIONS[i].replace('.', '_'))]
    l_nxt = globals()['LOOSE_VERSION_{0}'
                      ''.format(LOOSE_VERSIONS[i+1].replace('.', '_'))]
    var_name = 'DJANGO_{0}'.format(v.replace('.', '_'))
    globals()[var_name] = (l_cur <= LOOSE_DJANGO_VERSION < l_nxt)
    __all__.append(var_name)

# LTE list
LTE_VERSIONS = LOOSE_VERSIONS[:-1]

for i, v in enumerate(EXACT_VERSIONS):
    l_cur = globals()['LOOSE_VERSION_{0}'
                      ''.format(LOOSE_VERSIONS[i].replace('.', '_'))]
    var_name = 'DJANGO_LTE_{0}'.format(v.replace('.', '_'))
    globals()[var_name] = (LOOSE_DJANGO_MINOR_VERSION <= l_cur)
    __all__.append(var_name)

# GTE list
GTE_VERSIONS = LOOSE_VERSIONS[:-1]

for i, v in enumerate(EXACT_VERSIONS):
    l_cur = globals()['LOOSE_VERSION_{0}'
                      ''.format(LOOSE_VERSIONS[i].replace('.', '_'))]
    var_name = 'DJANGO_GTE_{0}'.format(v.replace('.', '_'))
    globals()[var_name] = (
        LOOSE_DJANGO_MINOR_VERSION >= l_cur
    )
    __all__.append(var_name)

__all__ = tuple(__all__)

# Clean up
try:
    del l_cur
    del l_nxt
    del var_name
    del i
    del v
except NameError:
    pass

del LooseVersion
del django
