# import unittest
# import mock
# # For Python3 >= 3.4
# try:
#     from importlib import reload
# # For Python3 < 3.4
# except ImportError as err:
#     try:
#         from imp import reload
#     except ImportError as err:
#         pass
#
# from django.urls import reverse
# from django.test import RequestFactory, TestCase
#
# from .base import log_info
#
# __title__ = 'django_nine.tests.test_versions'
# __author__ = 'Artur Barseghyan'
# __copyright__ = 'Copyright (c) 2015 Artur Barseghyan'
# __license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
# __all__ = ('ContextProcessorsTest',)
#
#
# class ContextProcessorsTest(TestCase):
#     """
#     Tests of ``django_nine.context_processors`` module.
#     """
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     @log_info
#     @mock.patch('django.get_version', mock.MagicMock(return_value='2.1'))
#     def test_django_2_1(self):
#         """
#         Tests as if we were using Django==2.1.
#         """
#         from django_nine import versions
#         reload(versions)
#
#         url = reverse('django_nine')
#         response = self.client.get(url)
#
#         import pytest; pytest.set_trace()
#
#
# if __name__ == "__main__":
#     unittest.main()
