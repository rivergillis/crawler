from bs4 import BeautifulSoup, SoupStrainer
from tld import get_tld
import requests
import re

# TODO: cover all cases where a url is empty
# TODO: create unit testing for these functions
# TODO: create a link data type that specifies form and other things
# TODO: this data can be serialized onto the disc using pickle


def get_root_url(link):
    """
    link: a string of a url in the form https://help.github.com/enterprise/2.7/user/
        utilized tld to obtain the subdomain and tld of the string in order to return a string
        of the form https://help.github.com/
    """
    if not link:
        return None

    url_tld = get_tld(link, as_object=True, fail_silently=True)
    if not url_tld:
        return None
    if link.startswith("https"):
        intro = "https://"
    else:
        intro = "http://"
    # some URLS do not contain a subdomain(e.g. https://google.com)
    if url_tld.subdomain:
        return intro + url_tld.subdomain + "." + url_tld.tld + "/"
    else:
        return intro + url_tld.tld + "/"


def remove_anchor(link):
    """
    link: a string of a url in form https://[tld]/asdf#anchor_point
    returns: a string of a url in form https://[tld]/asdf
    """
    # TODO: return none for empty string after split?
    if not link:
        return None
    return link.split("#")[0]

def up_a_directory(link):
    """
    link: a string of a url in the form https://rivergillis.com/test/
    returns: a string of a url in the form https://rivergillis.com/
    """
    if not link:
        return None
    removed_dir = link.rsplit('/', 2)[0]
    return removed_dir + '/'


def correct_trailing_slash(link):
    """
    link: a string of a url of any form
    returns: a string of a url of that same form with a trailing slash if possible
    ex: '/' -> '/'; '/asdf' -> '/asdf/'; '/asdf.html' -> '/asdf.html'
    '/asdf#sdfadsf' -> '/asdf/'; '#sdf' -> ''; '../' -> '../'
    'https://rivergillis.com' -> 'https://rivergillis.com/'
    """
    # print("correcting slash for", link)
    link = remove_anchor(link)
    if not link:
        return ''
    if link.endswith('/'):
        return link  # nothing needs to be done here, covers '/' case too

    url_tld = get_tld(link, as_object=True, fail_silently=True)
    pattern = re.compile(r'\.\w+')
    extensions = re.findall(pattern, link)

    def correct_rel(rel_link):  # for link of form: '/[anything]'
        if extensions and rel_link.endswith(extensions[-1]):
            # form: 'asdf.html'
            return rel_link
        return rel_link + '/'

    if url_tld:  # form: 'https://rivergillis.com/[anything else]'
        splitted = link.split(url_tld.tld)
        before_tld = splitted[0]
        after_tld = splitted[1]
        if not after_tld:
            return before_tld + url_tld.tld + '/'

        corrected = correct_rel(after_tld)
        return before_tld + url_tld.tld + corrected
    else:
        return correct_rel(link)


def clean_link(base_url, dirty_link, root_url):
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
    if not root_url:
        return None
    no_anchor = remove_anchor(dirty_link)
    if no_anchor.startswith('http://') or no_anchor.startswith('https://'):
        return correct_trailing_slash(no_anchor)
    else:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if no_anchor.endswith("/") and len(no_anchor) > 1:  # trailing slash
            no_anchor = no_anchor[:-1]
        if no_anchor.startswith("../"):
            # print('moving back, base', base_url)
            no_anchor = no_anchor[3:]
            base_url = base_url.rsplit("/", 1)[0]
            # print('splitted, base,',base_url)
        elif no_anchor.startswith("/"):  # root + extra
            return correct_trailing_slash(root_url + no_anchor[1:])
        else:
            base_url = base_url.rsplit("/", 1)[0]
            if base_url == "https:/":  # linked to an anchor of a base page
                return None
        full_link = base_url + "/" + no_anchor

    return correct_trailing_slash(full_link)


def clean_links(base_url, dirty_links):
    """
    base_url: a string of a url of an accessible (full) form, this is the url
        that contains the visited page which all other links were extracted from
    dirty_links: a list of strings of urls of an unaccessible form that were 
        extracted from the base_url page. See clean_link docstring for further details
    returns: a list of strings of urls of a fully accessible form
    """
    has_linked = {}
    full_links = []
    for link in dirty_links:
        cleaned = clean_link(base_url, link, get_root_url(base_url))
        if not cleaned:
            continue
        if has_linked.get(cleaned, False):
            continue
        if not has_html(cleaned):
            print(cleaned, "BUT THIS ISN'T AN HTML FILE!!!!!!!!!!")
            continue
        full_links.append(cleaned)
        has_linked[cleaned] = True
    return full_links


def has_html(url):
    """determines if a url ends with anything other than a directory, .html,
    .xhtml, or .php, requires a full url"""
    # BUG: files like https://github.com/rivergillis/crawler/blob/master/crawler.py are still html
    if url.endswith('/'):
        return True

    good_filetypes = [".html", ".xhtml", ".php"]
    pattern = re.compile(r'\.\w+\/*')
    url_tld = get_tld(url, fail_silently=True)
    if not url_tld:
        return False
    tld_split = url.split(url_tld)
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

have_visited = {}


def all_links(input_url):
    """
    input_url: a string of a url in a fully accessible form
    Downloads the web page attached to the string and searches
    for any links contained within. Visits each web page linked
    recursively and eventually returns a list of every link found
    on that page
    """
    
    # TODO: a valid html link begins with <!DOCTYPE html>
    # TODO: check for if we've visited https or http version (also maybe check for www or not)
    print("--------VISITING", input_url, "----------")
    response = requests.get(input_url)
    soup = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a'))

    links = []
    for link in soup:
        if link.has_attr('href'):
            if not (link['href'].startswith("#")):
                links.append(str(link['href']))

    full_links = clean_links(input_url, links)
    for link in full_links:
        print("found", link)
        if have_visited.get(link, False):
            print("but we already visited it!")
        else:
            have_visited[link] = True
            all_links(link)

    return full_links

# all_links("http://news.ycombinator.com/")
# url = "https://github.com/rivergillis/crawler/blob/master/crawler.py"
# all_links(url)
