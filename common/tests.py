from django.test import TestCase

from .models import *
from .functions import search_for_uuid

# Create your tests here.
class modelTests(TestCase):
    def setUp(self) -> None:
        self.new_port_range = port_ranges()
        self.new_port_range.start = "80"
        self.new_port_range.end = "80"
        self.new_port_range.transport = "tcp"
        self.new_port_range.save()

    def test_port_ranges(self):
        test_item = search_for_uuid(str(self.new_port_range.uuid))
        self.assertEqual(test_item,self.new_port_range)