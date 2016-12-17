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
        return None
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
        after_tld = splitted[1]
        if not after_tld:
            return before_tld + url_tld.tld + '/'

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

    def set_base(self, new_base):
        self.raw_base = new_base
        self.root_url = get_root_url(self.raw_base)


    def get_full_hyperlink(self):
        """
        :return: A string that is the cleaned hyperlink that can be used to access the html behind it
        """
        pass


    def is_html(self):
        """
        :return: A bool that is True only when the Link contains html (is not an mp4 file, for instance)
        """
        pass
