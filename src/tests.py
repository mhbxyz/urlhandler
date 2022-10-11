from unittest import TestCase

from urlhandler import URLHandler


class TestURLHandler(TestCase):
    def test__is_a_number(self):
        self.assertEqual(URLHandler._is_a_number('42'), 42)
        self.assertEqual(URLHandler._is_a_number('42.0'), 42.0)
        self.assertEqual(URLHandler._is_a_number('-42'), -42)
        self.assertEqual(URLHandler._is_a_number('-42.0'), -42.0)
        self.assertEqual(URLHandler._is_a_number('None'), None)

    def test_get_url(self):
        url = 'http://user:password@127.0.0.1?name=value&False=false&True=true&None=nulldict={1:"one","two":2,"three":"three"}#forward'
        self.assertEqual(URLHandler(url).get_url(), url)
