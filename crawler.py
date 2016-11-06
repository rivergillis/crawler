# returns a list of all of the links from a webpage
from bs4 import BeautifulSoup, SoupStrainer
from tld import get_tld
import requests
import re

def get_root_url(link):
    """Given a url in the form https://help.github.com/enterprise/2.7/user/, returns https://help.github.com/

    if not link[-1] == '/':
        link += '/'

    tld_pattern = re.compile(r'\.\w+\/')
    tld = re.findall(tld_pattern, link)[0]
    root = link.split(tld)[0] + tld
    return root
    """
    url_tld = get_tld(link, as_object=True, fail_silently=True)
    if not url_tld:
        return None
    if link.startswith("https"):
        intro = "https://"
    else:
        intro = "http://"
    if url_tld.subdomain:
        return intro + url_tld.subdomain + "." + url_tld.tld + "/"
    else:
        return intro + url_tld.tld + "/"


def remove_anchor(link):
    return link.split("#")[0]

def clean_link(base_url, dirty_link, root_url):
    if not root_url:
        return None
    no_anchor = remove_anchor(dirty_link)
    if no_anchor.startswith('http://') or no_anchor.startswith('https://'):
        return no_anchor
    else:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if no_anchor.endswith("/") and len(no_anchor) > 1: #trailing slash
            no_anchor = no_anchor[:-1]
        if no_anchor.startswith("../"):
            no_anchor = no_anchor[3:]
            base_url = base_url.rsplit("/", 2)[0]
        elif no_anchor.startswith("/"): # root + extra
            return root_url + no_anchor[1:]
        else:
            base_url = base_url.rsplit("/", 1)[0]
            if base_url == "https:/": # linked to an anchor of a base page
                return None
        full_link = base_url + "/" + no_anchor

    return full_link

def clean_links(base_url, dirty_links):
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
    #BUG: files like https://github.com/rivergillis/crawler/blob/master/crawler.py are still html

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

all_links("https://www.google.com/chrome/")
#url = "https://github.com/rivergillis/crawler/blob/master/crawler.py"
#all_links(url)
