import unittest
import crawler as c
import link as l


class TestLinkStringFunctions(unittest.TestCase):

    def test_get_root_url(self):
        self.assertEqual(l.get_root_url("https://help.github.com/enterprise/2.7/user/"), "https://help.github.com/")
        self.assertIsNone(l.get_root_url("/enterprise/2.7/user/"))
        self.assertEqual(l.get_root_url("http://help.github.com/enterprise/2.7/user/"), "http://help.github.com/")
        self.assertEqual(l.get_root_url("https://google.com/test/"), "https://google.com/")
        self.assertEqual(l.get_root_url("http://google.com/test/"), "http://google.com/")
        self.assertIsNone(l.get_root_url(""))
        self.assertIsNone(l.get_root_url(None))

    def test_remove_anchor(self):
        self.assertEqual(l.remove_anchor("http://rivergillis.com/f#anchor_point"), "http://rivergillis.com/f")
        self.assertEqual(l.remove_anchor("#asdf"), "")
        self.assertEqual(l.remove_anchor("asdf#asdf"), "asdf")
        self.assertIsNone(l.remove_anchor(None))

    def test_correct_trailing_slash(self):
        self.assertEqual(l.correct_trailing_slash("/"), "/")
        self.assertEqual(l.correct_trailing_slash("/asdf/"), "/asdf/")
        self.assertEqual(l.correct_trailing_slash("/asdf.html"), "/asdf.html")
        self.assertEqual(l.correct_trailing_slash("/asdf#asdf"), "/asdf/")
        self.assertEqual(l.correct_trailing_slash("#asdf"), "")
        self.assertEqual(l.correct_trailing_slash("../"), "../")
        self.assertEqual(l.correct_trailing_slash("../asdf"), "../asdf/")
        self.assertEqual(l.correct_trailing_slash("http://rivergillis.com"), "http://rivergillis.com/")
        self.assertEqual(l.correct_trailing_slash("./test"), "./test/")
        self.assertEqual(l.correct_trailing_slash("./test.html"), "./test.html")
        self.assertEqual(l.correct_trailing_slash("./test#asdf"), "./test/")
        self.assertEqual(l.correct_trailing_slash("./test.html#adsf"), "./test.html")
        self.assertEqual(l.correct_trailing_slash("./"), "./")

    def test_up_a_directory(self):
        self.assertIsNone(l.up_a_directory(None))
        self.assertEqual(l.up_a_directory("https://rivergillis.com/river/"), "https://rivergillis.com/")
        self.assertEqual(l.up_a_directory("http://rivergillis.co.uk/river/river/"), "http://rivergillis.co.uk/river/")


class TestLinkObjectMethods(unittest.TestCase):

    def test_initialize(self):
        test_link = l.Link("raw_value", "raw_base")
        self.assertEqual(test_link.raw_value, "raw_value")
        self.assertEqual(test_link.raw_base, "raw_base")

    def test_get_root_url(self):
        test_link = l.Link("rel_link", "https://help.github.com/enterprise/2.7/user/")
        self.assertEqual(test_link.root_url, "https://help.github.com/")
        test_link.set_base("http://www.google.co.uk/")
        self.assertEqual(test_link.root_url, "http://www.google.co.uk/")


class TestLinkCrawlerMethods(unittest.TestCase):

    def test_get_root_url(self):
        self.assertEqual(c.get_root_url("https://help.github.com/enterprise/2.7/user/"), "https://help.github.com/")
        self.assertIsNone(c.get_root_url("/enterprise/2.7/user/"))
        self.assertEqual(c.get_root_url("http://help.github.com/enterprise/2.7/user/"), "http://help.github.com/")
        self.assertEqual(c.get_root_url("https://google.com/test/"), "https://google.com/")
        self.assertEqual(c.get_root_url("http://google.com/test/"), "http://google.com/")
        self.assertIsNone(c.get_root_url(""))
        self.assertIsNone(c.get_root_url(None))

    def test_remove_anchor(self):
        self.assertEqual(c.remove_anchor("http://rivergillis.com/f#anchor_point"), "http://rivergillis.com/f")
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
        self.assertEqual(c.correct_trailing_slash("http://rivergillis.com"), "http://rivergillis.com/")
        self.assertEqual(c.correct_trailing_slash("./test"), "./test/")
        self.assertEqual(c.correct_trailing_slash("./test.html"), "./test.html")
        self.assertEqual(c.correct_trailing_slash("./test#asdf"), "./test/")
        self.assertEqual(c.correct_trailing_slash("./test.html#adsf"), "./test.html")
        self.assertEqual(c.correct_trailing_slash("./"), "./")

    def test_up_a_directory(self):
        self.assertIsNone(c.up_a_directory(None))
        self.assertEqual(c.up_a_directory("https://rivergillis.com/river/"), "https://rivergillis.com/")
        self.assertEqual(c.up_a_directory("http://rivergillis.co.uk/river/river/"), "http://rivergillis.co.uk/river/")

    def test_remove_self_ref(self):
        self.assertIsNone(c.remove_self_ref(None))
        self.assertEqual(c.remove_self_ref("./test"), "test")
        self.assertEqual(c.remove_self_ref("../test"), "../test")
        self.assertEqual(c.remove_self_ref("././test/"), "./test/")

    def test_clean_link(self):
        base_url = "http://rivergillis.com/"
        # note: make sure to test get_root_url first
        root_url = c.get_root_url(base_url)
        self.assertEqual(c.clean_link(base_url, "/index", root_url), "http://rivergillis.com/index/")
        self.assertEqual(c.clean_link(base_url, "/index.html", root_url), "http://rivergillis.com/index.html")
        self.assertEqual(c.clean_link(base_url, "/index#sadf", root_url), "http://rivergillis.com/index/")
        # self.assertEqual(c.clean_link(base_url, "../", root_url), ?)
        # self.assertEqual(c.clean_link(base_url, "../../", root_url), ?)
        self.assertEqual(c.clean_link(base_url, "#asdf", root_url), "http://rivergillis.com/")
        self.assertEqual(c.clean_link(base_url, "index.html", root_url), "http://rivergillis.com/index.html")
        self.assertEqual(c.clean_link(base_url, "index", root_url), "http://rivergillis.com/index/")
        base_url = "https://www.rivergillis.co.uk/test/3.5/"
        root_url = c.get_root_url(base_url)
        self.assertEqual(c.clean_link(base_url, "/index", root_url), "https://www.rivergillis.co.uk/index/")
        self.assertEqual(c.clean_link(base_url, "/index.html", root_url), "https://www.rivergillis.co.uk/index.html")
        self.assertEqual(c.clean_link(base_url, "/index#sadf", root_url), "https://www.rivergillis.co.uk/index/")
        self.assertEqual(c.clean_link(base_url, "../", root_url), "https://www.rivergillis.co.uk/test/")
        self.assertEqual(c.clean_link(base_url, "../index", root_url), "https://www.rivergillis.co.uk/test/index/")
        self.assertEqual(c.clean_link(base_url, "../index#asdf", root_url), "https://www.rivergillis.co.uk/test/index/")
        self.assertEqual(c.clean_link(base_url, "../index.html", root_url), "https://www.rivergillis.co.uk/test/index.html")
        self.assertEqual(c.clean_link(base_url, "../../", root_url), "https://www.rivergillis.co.uk/")
        self.assertEqual(c.clean_link(base_url, "#asdf", root_url), "https://www.rivergillis.co.uk/test/3.5/")
        self.assertEqual(c.clean_link(base_url, "index.html", root_url), "https://www.rivergillis.co.uk/test/3.5/index.html")
        self.assertEqual(c.clean_link(base_url, "index", root_url), "https://www.rivergillis.co.uk/test/3.5/index/")


        self.assertEqual(c.clean_link(base_url, "./foo", root_url), "https://www.rivergillis.co.uk/test/3.5/foo/")
        self.assertEqual(c.clean_link(base_url, "./foo.html", root_url), "https://www.rivergillis.co.uk/test/3.5/foo.html")
        self.assertEqual(c.clean_link(base_url, "./foo.html#asdf", root_url), "https://www.rivergillis.co.uk/test/3.5/foo.html")
        self.assertEqual(c.clean_link(base_url, "./../foo", root_url), "https://www.rivergillis.co.uk/test/foo/")
        self.assertEqual(c.clean_link(base_url, ".././foo", root_url), "https://www.rivergillis.co.uk/test/foo/")


if __name__ == '__main__':
    unittest.main()
