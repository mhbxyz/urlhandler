from unittest import TestCase

from urlhandler import URLHandler


class TestURLHandler(TestCase):
    def test__is_a_number(self):
        self.assertEqual(URLHandler._is_a_number('42'), 42)
        self.assertEqual(URLHandler._is_a_number('42.0'), 42.0)
        self.assertEqual(URLHandler._is_a_number('-42'), -42)
        self.assertEqual(URLHandler._is_a_number('-42.0'), -42.0)
        self.assertEqual(URLHandler._is_a_number('None'), None)
