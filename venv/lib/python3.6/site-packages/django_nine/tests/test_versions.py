import unittest
import mock
# For Python3 >= 3.4
try:
    from importlib import reload
# For Python3 < 3.4
except ImportError as err:
    try:
        from imp import reload
    except ImportError as err:
        pass

from .base import log_info

__title__ = 'django_nine.tests.test_versions'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2015 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('VersionsTest',)


class VersionsTest(unittest.TestCase):
    """
    Tests of ``django_nine.versions`` module.
    """
    def setUp(self):
        pass

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.4.21'))
    def test_django_1_4_21(self):
        """
        Tests as if we were using Django==1.4.21.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertTrue(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)

        # Less than or equal matching
        self.assertTrue(versions.DJANGO_LTE_1_4)
        self.assertTrue(versions.DJANGO_LTE_1_5)
        self.assertTrue(versions.DJANGO_LTE_1_6)
        self.assertTrue(versions.DJANGO_LTE_1_7)
        self.assertTrue(versions.DJANGO_LTE_1_8)
        self.assertTrue(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertFalse(versions.DJANGO_GTE_1_5)
        self.assertFalse(versions.DJANGO_GTE_1_6)
        self.assertFalse(versions.DJANGO_GTE_1_7)
        self.assertFalse(versions.DJANGO_GTE_1_8)
        self.assertFalse(versions.DJANGO_GTE_1_9)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.5.5'))
    def test_django_1_5_5(self):
        """
        Tests as if we were using Django==1.5.5.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertTrue(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertTrue(versions.DJANGO_LTE_1_5)
        self.assertTrue(versions.DJANGO_LTE_1_6)
        self.assertTrue(versions.DJANGO_LTE_1_7)
        self.assertTrue(versions.DJANGO_LTE_1_8)
        self.assertTrue(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertFalse(versions.DJANGO_GTE_1_6)
        self.assertFalse(versions.DJANGO_GTE_1_7)
        self.assertFalse(versions.DJANGO_GTE_1_8)
        self.assertFalse(versions.DJANGO_GTE_1_9)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.6.5'))
    def test_django_1_6_5(self):
        """
        Tests as if we were using Django==1.6.5.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertTrue(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertTrue(versions.DJANGO_LTE_1_6)
        self.assertTrue(versions.DJANGO_LTE_1_7)
        self.assertTrue(versions.DJANGO_LTE_1_8)
        self.assertTrue(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertFalse(versions.DJANGO_GTE_1_7)
        self.assertFalse(versions.DJANGO_GTE_1_8)
        self.assertFalse(versions.DJANGO_GTE_1_9)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.7.5'))
    def test_django_1_7_5(self):
        """
        Tests as if we were using Django==1.7.5.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertTrue(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertTrue(versions.DJANGO_LTE_1_7)
        self.assertTrue(versions.DJANGO_LTE_1_8)
        self.assertTrue(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertFalse(versions.DJANGO_GTE_1_8)
        self.assertFalse(versions.DJANGO_GTE_1_9)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.8.a1'))
    def test_django_1_8_a1(self):
        """
        Tests as if we were using Django==1.8.a1.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertTrue(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertTrue(versions.DJANGO_LTE_1_8)
        self.assertTrue(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertFalse(versions.DJANGO_GTE_1_9)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.10'))
    def test_django_1_10(self):
        """
        Tests as if we were using Django==1.10.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertTrue(versions.DJANGO_1_10)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='1.11'))
    def test_django_1_11(self):
        """
        Tests as if we were using Django==1.11.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertFalse(versions.DJANGO_1_10)
        self.assertTrue(versions.DJANGO_1_11)
        self.assertFalse(versions.DJANGO_2_0)
        self.assertFalse(versions.DJANGO_2_1)
        self.assertFalse(versions.DJANGO_2_2)
        self.assertFalse(versions.DJANGO_3_0)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)
        self.assertFalse(versions.DJANGO_LTE_1_10)
        self.assertTrue(versions.DJANGO_LTE_1_11)
        self.assertTrue(versions.DJANGO_LTE_2_0)
        self.assertTrue(versions.DJANGO_LTE_2_1)
        self.assertTrue(versions.DJANGO_LTE_2_2)
        self.assertTrue(versions.DJANGO_LTE_3_0)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)
        self.assertTrue(versions.DJANGO_GTE_1_11)
        self.assertFalse(versions.DJANGO_GTE_2_0)
        self.assertFalse(versions.DJANGO_GTE_2_1)
        self.assertFalse(versions.DJANGO_GTE_2_2)
        self.assertFalse(versions.DJANGO_GTE_3_0)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='2.0'))
    def test_django_2_0(self):
        """
        Tests as if we were using Django==2.0.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertFalse(versions.DJANGO_1_10)
        self.assertFalse(versions.DJANGO_1_11)
        self.assertTrue(versions.DJANGO_2_0)
        self.assertFalse(versions.DJANGO_2_1)
        self.assertFalse(versions.DJANGO_2_2)
        self.assertFalse(versions.DJANGO_3_0)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)
        self.assertFalse(versions.DJANGO_LTE_1_10)
        self.assertFalse(versions.DJANGO_LTE_1_11)
        self.assertTrue(versions.DJANGO_LTE_2_0)
        self.assertTrue(versions.DJANGO_LTE_2_1)
        self.assertTrue(versions.DJANGO_LTE_2_2)
        self.assertTrue(versions.DJANGO_LTE_3_0)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)
        self.assertTrue(versions.DJANGO_GTE_1_11)
        self.assertTrue(versions.DJANGO_GTE_2_0)
        self.assertFalse(versions.DJANGO_GTE_2_1)
        self.assertFalse(versions.DJANGO_GTE_2_2)
        self.assertFalse(versions.DJANGO_GTE_3_0)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='2.1'))
    def test_django_2_1(self):
        """
        Tests as if we were using Django==2.1.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertFalse(versions.DJANGO_1_10)
        self.assertFalse(versions.DJANGO_1_11)
        self.assertFalse(versions.DJANGO_2_0)
        self.assertTrue(versions.DJANGO_2_1)
        self.assertFalse(versions.DJANGO_2_2)
        self.assertFalse(versions.DJANGO_3_0)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)
        self.assertFalse(versions.DJANGO_LTE_1_10)
        self.assertFalse(versions.DJANGO_LTE_1_11)
        self.assertFalse(versions.DJANGO_LTE_2_0)
        self.assertTrue(versions.DJANGO_LTE_2_1)
        self.assertTrue(versions.DJANGO_LTE_2_2)
        self.assertTrue(versions.DJANGO_LTE_3_0)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)
        self.assertTrue(versions.DJANGO_GTE_1_11)
        self.assertTrue(versions.DJANGO_GTE_2_0)
        self.assertTrue(versions.DJANGO_GTE_2_1)
        self.assertFalse(versions.DJANGO_GTE_2_2)
        self.assertFalse(versions.DJANGO_GTE_3_0)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='2.2'))
    def test_django_2_2(self):
        """
        Tests as if we were using Django==2.2.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertFalse(versions.DJANGO_1_10)
        self.assertFalse(versions.DJANGO_1_11)
        self.assertFalse(versions.DJANGO_2_0)
        self.assertFalse(versions.DJANGO_2_1)
        self.assertTrue(versions.DJANGO_2_2)
        self.assertFalse(versions.DJANGO_3_0)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)
        self.assertFalse(versions.DJANGO_LTE_1_10)
        self.assertFalse(versions.DJANGO_LTE_1_11)
        self.assertFalse(versions.DJANGO_LTE_2_0)
        self.assertFalse(versions.DJANGO_LTE_2_1)
        self.assertTrue(versions.DJANGO_LTE_2_2)
        self.assertTrue(versions.DJANGO_LTE_3_0)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)
        self.assertTrue(versions.DJANGO_GTE_1_11)
        self.assertTrue(versions.DJANGO_GTE_2_0)
        self.assertTrue(versions.DJANGO_GTE_2_1)
        self.assertTrue(versions.DJANGO_GTE_2_2)
        self.assertFalse(versions.DJANGO_GTE_3_0)

    @log_info
    @mock.patch('django.get_version', mock.MagicMock(return_value='3.0'))
    def test_django_3_0(self):
        """
        Tests as if we were using Django==3.0.
        """
        from django_nine import versions
        reload(versions)

        # Exact version matching
        self.assertFalse(versions.DJANGO_1_4)
        self.assertFalse(versions.DJANGO_1_5)
        self.assertFalse(versions.DJANGO_1_6)
        self.assertFalse(versions.DJANGO_1_7)
        self.assertFalse(versions.DJANGO_1_8)
        self.assertFalse(versions.DJANGO_1_9)
        self.assertFalse(versions.DJANGO_1_10)
        self.assertFalse(versions.DJANGO_1_11)
        self.assertFalse(versions.DJANGO_2_0)
        self.assertFalse(versions.DJANGO_2_1)
        self.assertFalse(versions.DJANGO_2_2)
        self.assertTrue(versions.DJANGO_3_0)

        # Less than or equal matching
        self.assertFalse(versions.DJANGO_LTE_1_4)
        self.assertFalse(versions.DJANGO_LTE_1_5)
        self.assertFalse(versions.DJANGO_LTE_1_6)
        self.assertFalse(versions.DJANGO_LTE_1_7)
        self.assertFalse(versions.DJANGO_LTE_1_8)
        self.assertFalse(versions.DJANGO_LTE_1_9)
        self.assertFalse(versions.DJANGO_LTE_1_10)
        self.assertFalse(versions.DJANGO_LTE_1_11)
        self.assertFalse(versions.DJANGO_LTE_2_0)
        self.assertFalse(versions.DJANGO_LTE_2_1)
        self.assertFalse(versions.DJANGO_LTE_2_2)
        self.assertTrue(versions.DJANGO_LTE_3_0)

        # Greater than or equal matching
        self.assertTrue(versions.DJANGO_GTE_1_4)
        self.assertTrue(versions.DJANGO_GTE_1_5)
        self.assertTrue(versions.DJANGO_GTE_1_6)
        self.assertTrue(versions.DJANGO_GTE_1_7)
        self.assertTrue(versions.DJANGO_GTE_1_8)
        self.assertTrue(versions.DJANGO_GTE_1_9)
        self.assertTrue(versions.DJANGO_GTE_1_10)
        self.assertTrue(versions.DJANGO_GTE_1_11)
        self.assertTrue(versions.DJANGO_GTE_2_0)
        self.assertTrue(versions.DJANGO_GTE_2_1)
        self.assertTrue(versions.DJANGO_GTE_2_2)
        self.assertTrue(versions.DJANGO_GTE_3_0)


if __name__ == "__main__":
    unittest.main()
