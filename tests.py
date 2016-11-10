import unittest
import crawler as c


class TestLinkMethods(unittest.TestCase):

    def test_get_root_url(self):
        self.assertEqual(c.get_root_url("https://help.github.com/enterprise/2.7/user/"), "https://help.github.com/")
        self.assertIsNone(c.get_root_url("/enterprise/2.7/user/"))
        self.assertEqual(c.get_root_url("http://help.github.com/enterprise/2.7/user/"), "http://help.github.com/")
        self.assertEqual(c.get_root_url("https://google.com/test/"), "https://google.com/")
        self.assertEqual(c.get_root_url("http://google.com/test/"), "http://google.com/")
        self.assertIsNone(c.get_root_url(""))
        self.assertIsNone(c.get_root_url(None))

    def test_remove_anchor(self):
        self.assertEqual(c.remove_anchor("https://rivergillis.com/f#anchor_point"), "https://rivergillis.com/f")
        self.assertEqual(c.remove_anchor("#asdf"), "")
        self.assertEqual(c.remove_anchor("asdf#asdf"), "asdf")
        self.assertIsNone(c.remove_anchor(None))

    def test_correct_trailing_slash(self):
        self.assertEqual(c.correct_trailing_slash("/"), "/")
        self.assertEqual(c.correct_trailing_slash("/asdf/"), "/asdf/")
        self.assertEqual(c.correct_trailing_slash("/asdf.html"), "/asdf.html")
        self.assertEqual(c.correct_trailing_slash("/asdf#asdf"), "/asdf/")
        self.assertEqual(c.correct_trailing_slash("#asdf"), "")
        self.assertEqual(c.correct_trailing_slash("../"), "../")
        self.assertEqual(c.correct_trailing_slash("../asdf"), "../asdf/")
        self.assertEqual(c.correct_trailing_slash("https://rivergillis.com"), "https://rivergillis.com/")

        """
        link: a string of a url of any form
        returns: a string of a url of that same form with a trailing slash if possible
        ex: '/' -> '/'; '/asdf' -> '/asdf/'; '/asdf.html' -> '/asdf.html'
        '/asdf#sdfadsf' -> '/asdf/'; '#sdf' -> ''; '../' -> '../'
        'https://rivergillis.com' -> 'https://rivergillis.com/'
        """

if __name__ == '__main__':
    unittest.main()
