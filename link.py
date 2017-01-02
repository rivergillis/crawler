"""
This is the file to be used for the link type object for crawler.py
As well as Link String methods used to help the Link object
Author: Jameson Gillis
"""
from tld import get_tld
import re


# this can stay outside of the Link class
def remove_anchor(link_string):
    """
    This removes the anchor point from a URL string
    In practice, this shouldn't be called directly and should be called through correct_trailing_slash
    link: a string of a url in form https://[tld]/asdf#anchor_point
    returns: a string of a url in form https://[tld]/asdf
    """
    # TODO: return none for empty string after split?
    if not link_string:
        return ''
    return link_string.split("#")[0]

def correct_trailing_slash(link_string):
    """
    link: a string of a url of any form
    returns: a string of a url of that same form with a trailing slash if possible
    ex: '/' -> '/'; '/asdf' -> '/asdf/'; '/asdf.html' -> '/asdf.html'
    '/asdf#sdfadsf' -> '/asdf/'; '#sdf' -> ''; '../' -> '../'
    'https://rivergillis.com' -> 'https://rivergillis.com/'
    """
    # print("correcting slash for", link)
    link_string = remove_anchor(link_string)
    if not link_string:
        return ''
    if link_string.endswith('/'):
        return link_string  # nothing needs to be done here, covers '/' case too

    url_tld = get_tld(link_string, as_object=True, fail_silently=True)
    pattern = re.compile(r'\.\w+')
    # we only care about the last element of extensions, as it will be the .com/.html portion if it exists
    extensions = re.findall(pattern, link_string)

    def correct_rel(rel_link):  # for link of form: '/[anything]'
        # form: '/asdf.html'
        if extensions and rel_link.endswith(extensions[-1]):
            return rel_link
        # form: '/asdf/'
        return rel_link + '/'

    if url_tld:  # form: 'https://rivergillis.com/[anything else]'
        splitted = link_string.split(url_tld.tld)
        before_tld = splitted[0]
        if len(splitted) <= 1:
            return before_tld + url_tld.tld + '/'

        after_tld = splitted[1]

        corrected = correct_rel(after_tld)
        return before_tld + url_tld.tld + corrected
    else:
        return correct_rel(link_string)


def get_root_url(link_string):
    """
    Will always return a string with a correct trailing slash or None for invalid string
    link: a string of a url in the form https://help.github.com/enterprise/2.7/user/
        utilized tld to obtain the subdomain and tld of the string in order to return a string
        of the form https://help.github.com/
    """
    if not link_string:
        return None

    url_tld = get_tld(link_string, as_object=True, fail_silently=True)
    if not url_tld:
        return None
    if link_string.startswith("https"):
        intro = "https://"
    else:
        intro = "http://"
    # some URLS do not contain a subdomain(e.g. https://google.com)
    if url_tld.subdomain:
        return intro + url_tld.subdomain + "." + url_tld.tld + "/"
    else:
        return intro + url_tld.tld + "/"


def up_a_directory(link_string):
    """
    link: a string of a url in the form https://rivergillis.com/test/
    returns: a string of a url in the form https://rivergillis.com/
    """
    if not link_string:
        return None
    if link_string == get_root_url(link_string):
        raise ValueError(link_string, " is the same as its base and thus cannot move up a dir")
    removed_dir = link_string.rsplit('/', 2)[0] + '/'
    return removed_dir


def remove_self_ref(link_string):
    """
    :param link_string: a string of a url beginning with './foo'
    :return: a string of a url of the form 'foo'
    """
    if not link_string:
        return None
    elif link_string.startswith('./'):
        return link_string[2:]
    else:
        return link_string


class Link(object):
    """
    The Link object is to be used in crawler.py to handle all types of links obtained while searching html
    Links have:
        raw_value: a string representing the input value that the Link was created with
        raw_base: a string representing the full_hyperlink that the raw_value was found on
        full_hyperlink: a string value representing the completed, cleaned hyperlink to be used for accessing
    Links have many more things necessary to create the above values, those are documented by member definition
    """
    def __init__(self, raw_value, raw_base):
        self.raw_value = raw_value
        self.raw_base = raw_base

        self.root_url = get_root_url(self.raw_base)
        self.full_hyperlink = self.get_full_hyperlink()

    def set_base(self, new_base):
        self.raw_base = new_base
        self.root_url = get_root_url(self.raw_base)
        self.full_hyperlink = self.get_full_hyperlink()

    def set_raw_value(self, new_raw):
        # This should probably be used only for testing
        self.raw_value = new_raw
        self.full_hyperlink = self.get_full_hyperlink()

    def is_ssl(self):
        """
        :return: True if the full hyperlink begins with https, false otherwise
        """
        if self.raw_value.startswith("https"):
            return True
        elif self.raw_value.startswith("http"):
            return False
        else:
            return self.raw_base.startswith("https")

    def get_full_hyperlink(self):
        """
        base_url: a string of a url in form of a accessible webpage
            that is to say base_url is the web page that was succesfully visited and
            had links extracted from it
        dirty_link: a string of a url that was extracted from the base_url webpage
            possible forms for dirty_link include '../[link]', '/[link]', '[link]', all of which
            are links that refer to the root or base url. It could also be a full link to an
            external web_page.
        root_url: a string of a url containing the subdomain followed by the domain of the url,
            essentially, this url would direct to the top level of the website
        """
        # print("cleaning", dirty_link, "with base", base_url, "with root", root_url)
        if not self.root_url:
            raise ValueError("Error, this Link object has no root_url. Cannot make a full_hyperlink.")
        no_anchor = remove_anchor(self.raw_value)
        if no_anchor.startswith('http://') or no_anchor.startswith('https://'):
            return correct_trailing_slash(no_anchor)
        else:
            c_base_url = correct_trailing_slash(self.raw_base)
            c_dirty = correct_trailing_slash(no_anchor)

            if c_dirty.startswith("//"):
                if self.is_ssl():
                    return "https:" + c_dirty
                else:
                    return "http:" + c_dirty

            while c_dirty.startswith("./"):
                c_dirty = remove_self_ref(c_dirty)
            while c_dirty.startswith("../"):
                c_base_url = up_a_directory(c_base_url)
                # This is the case where the link is just '../'
                if len(c_dirty) == 3:  # this could lead to a bug?
                    return correct_trailing_slash(c_base_url)
                else:
                    c_dirty = c_dirty[3:]
                    # now check for and remove './'
                    c_dirty = remove_self_ref(c_dirty)
            while c_dirty.startswith("./"):
                c_dirty = remove_self_ref(c_dirty)

            if c_dirty.startswith("/"):  # root + extra
                return correct_trailing_slash(self.root_url + c_dirty[1:])
            else:
                return correct_trailing_slash(c_base_url + c_dirty)

    def is_html(self):
        """determines if a url ends with anything other than a directory, .html,
        .xhtml, or .php, requires a full url"""
        # BUG: files like https://github.com/rivergillis/crawler/blob/master/crawler.py are still html
        if self.full_hyperlink.endswith('/'):
            return True

        good_filetypes = [".html", ".xhtml", ".php"]
        pattern = re.compile(r'\.\w+\/*')
        url_tld = get_tld(self.full_hyperlink, fail_silently=True)
        if not url_tld:
            return False
        tld_split = self.full_hyperlink.split(url_tld)
        if len(tld_split) > 1:
            after_tld = tld_split[1]
            extensions = re.findall(pattern, after_tld)

            if not extensions:
                return True
            if not after_tld.endswith(extensions[-1]):
                return True
            if extensions[-1] not in good_filetypes:
                return False
        return True

    def __str__(self):
        """
        :return: string representation of the full hyperlink
        """
        return self.full_hyperlink

    def equals_link(self, other, ignore_https=True):
        """
        :param other: Link we are comparing to determine if equal
        :param ignore_https: Links with http are equal to https links if True
        :return:
        """
        if ignore_https:
            # cut off everything after the http[s] and look at only that part
            return self.full_hyperlink.split(":", 1)[1] == other.full_hyperlink.split(":", 1)[1]
        else:
            return self.full_hyperlink == other.full_hyperlink

    def __hash__(self):
        return hash(self.full_hyperlink)

    def __eq__(self, other):
        return self.full_hyperlink == other.full_hyperlink

    def __ne__(self, other):
        return not(self == other)
