# returns a list of all of the links from a webpage
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

def remove_anchor(link):
    return link.split("#")[0]

def clean_link(base_url, dirty_link):
    no_anchor = remove_anchor(dirty_link)
    if no_anchor.startswith('http://') or no_anchor.startswith('https://'):
        return no_anchor
    else:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if no_anchor.endswith("/"): #trailing slash
            no_anchor = no_anchor[:-1]
        if no_anchor.startswith("../"):
            no_anchor = no_anchor[3:]
            base_url = base_url.rsplit("/", 2)[0]
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
        cleaned = clean_link(base_url, link)
        if not cleaned:
            continue
        if has_linked.get(cleaned, False):
            continue
        full_links.append(cleaned)
        has_linked[cleaned] = True
    return full_links

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

url = "https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse"
all_links(url)
