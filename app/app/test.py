"""
Simple tests
"""
from django.test import SimpleTestCase
from app import clac

class CalcTest(SimpleTestCase):
    """Tests for calc function."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        self.assertEqual(clac.add(5,3),8)