from bs4 import BeautifulSoup, SoupStrainer
from tld import get_tld
import requests
import re

# TODO: cover all cases where a url is empty
# TODO: create unit testing for these functions
# TODO: create a link data type that specifies form and other things
# TODO: this data can be serialized onto the disc using pickle


def move_up_dirs(link, root_url):
    """
    :param link: a link of url with an arbitrary number of dirs to traverse (ex: './../././../test')
    :param root_url: a link of the root url from which link was linked
    :return:
    """
    pass

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

if __name__ == "__main__":
    url = "https://github.com/rivergillis/crawler/blob/master/crawler.py"
    all_links(url)
