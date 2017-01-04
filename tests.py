import unittest
import crawler as c
import link as l
import page as p


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
        self.assertEqual(l.correct_trailing_slash("//stackoverflow.com"), "//stackoverflow.com/")

    def test_up_a_directory(self):
        self.assertIsNone(l.up_a_directory(None))
        self.assertEqual(l.up_a_directory("https://rivergillis.com/river/"), "https://rivergillis.com/")
        self.assertEqual(l.up_a_directory("http://rivergillis.co.uk/river/river/"), "http://rivergillis.co.uk/river/")

    def test_remove_self_ref(self):
        self.assertIsNone(l.remove_self_ref(None))
        self.assertEqual(l.remove_self_ref("./test"), "test")
        self.assertEqual(l.remove_self_ref("../test"), "../test")
        self.assertEqual(l.remove_self_ref("././test/"), "./test/")


class TestLinkObjectMethods(unittest.TestCase):

    def test_get_root_url(self):
        test_link = l.Link("rel_link", "https://help.github.com/enterprise/2.7/user/")
        self.assertEqual(test_link.root_url, "https://help.github.com/")
        test_link.set_base("http://www.google.co.uk/")
        self.assertEqual(test_link.root_url, "http://www.google.co.uk/")

    def test_get_full_hyperlink(self):
        test_link = l.Link("/index", "http://rivergillis.com/")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/index/")
        test_link.set_raw_value("/index.html")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/index.html")
        test_link.set_raw_value("/index#sadf")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/index/")
        test_link.set_raw_value("//stackoverflow.com")
        self.assertEqual(test_link.full_hyperlink, "http://stackoverflow.com/")
        test_link.set_raw_value("/")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/")

        # self.assertEqual(c.clean_link(base_url, "../", root_url), ?)
        # self.assertEqual(c.clean_link(base_url, "../../", root_url), ?)

        test_link.set_raw_value("#sadf")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/")
        test_link.set_raw_value("index.html")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/index.html")
        test_link.set_raw_value("index#sdf")
        self.assertEqual(test_link.full_hyperlink, "http://rivergillis.com/index/")

        test_link.set_base("https://www.rivergillis.co.uk/test/3.5/")
        test_link.set_raw_value("/index")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/index/")
        test_link.set_raw_value("/index.html")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/index.html")
        test_link.set_raw_value("/index#sadf")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/index/")
        test_link.set_raw_value("//stackoverflow.com")
        self.assertEqual(test_link.full_hyperlink, "https://stackoverflow.com/")

        test_link.set_raw_value("../")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/")
        test_link.set_raw_value("../index")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/index/")
        test_link.set_raw_value("../index#asdf")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/index/")
        test_link.set_raw_value("../index.html")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/index.html")
        test_link.set_raw_value("../../")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/")
        test_link.set_raw_value("#asdf")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/")
        test_link.set_raw_value("index.html")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/index.html")
        test_link.set_raw_value("index")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/index/")

        test_link.set_raw_value("./foo")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/foo/")
        test_link.set_raw_value("./foo.html")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/foo.html")
        test_link.set_raw_value("./foo.html#asdf")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/3.5/foo.html")
        test_link.set_raw_value("./../foo")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/foo/")
        test_link.set_raw_value(".././foo")
        self.assertEqual(test_link.full_hyperlink, "https://www.rivergillis.co.uk/test/foo/")

    def test_is_ssl(self):
        link = l.Link("index", "http://stackoverflow.com/")
        self.assertFalse(link.is_ssl())
        link.set_base("https://stackoverflow.com/")
        self.assertTrue(link.is_ssl())
        link.set_raw_value("http://rivergillis.com/")
        self.assertFalse(link.is_ssl())

    def test_equals_link(self):
        first = l.Link("index", "http://www.rivergillis.co.uk/test/")
        second = l.Link("./index", "https://www.rivergillis.co.uk/test/")
        self.assertFalse(first.equals_link(second, False))
        self.assertTrue(first.equals_link(second))


class TestPageMethods(unittest.TestCase):
    # These will fail if I update the about me page

    def test_page_creation(self):
        page = p.Page("http://rivergillis.com/about/")
        self.assertEqual(page.domain, "http://rivergillis.com/")

    def test_page_create_links(self):
        # This test is very slow
        page = p.Page("http://rivergillis.com/about/")
        correct_link_str = {"http://rivergillis.com/", "http://rivergillis.com/about/", "http://rivergillis.com/posts/",
                            "http://rivergillis.com/feed.xml",
                            "https://github.com/rivergillis", "https://twitter.com/rivergillis",
                            "http://rivergillis.com/resume.pdf"}
        correct_links = set()
        for link in correct_link_str:
            correct_links.add(l.Link(link, "http://rivergillis.com/about/"))

        self.assertEqual(page.get_links(), correct_links)


class TestLinkCrawlerMethods(unittest.TestCase):

    def test_clean_link(self):
        pass


if __name__ == '__main__':
    unittest.main()
