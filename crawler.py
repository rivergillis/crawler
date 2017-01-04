from bs4 import BeautifulSoup, SoupStrainer
from link import Link
from page import Page
import requests

# TODO: cover all cases where a url is empty
# TODO: create unit testing for these functions
# TODO: create a link data type that specifies form and other things
# TODO: this data can be serialized onto the disc using pickle
# TODO: Fix for http://miniorange.com/fraud/
# TODO: Make a page object, this object contains a set of links from that page, if two pages on a domain have the same set of links (use set minus), stop and drop the page


def move_up_dirs(link, root_url):
    """
    :param link: a link of url with an arbitrary number of dirs to traverse (ex: './../././../test')
    :param root_url: a link of the root url from which link was linked
    :return:
    """
    pass

grabbed_links = []  # Grabbed links contains the list of upcoming Links to be crawled
has_grabbed = set()  # has_grabbed contains a set of Links that we have already grabbed
page_counts = {}   # page_counts contains the number of times a certain page has been grabbed (Page -> Count)
pages_by_links = {}  # pages_by_links has a page object for a corresponding link object (Link -> Page)


def begin_crawl(input_url):
    """
    calls crawl and maintains calling it in a while loop, keeping track of the # of links grabbed
    :param input_url: the first link to begin crawling on, a string
    :return: the length of the crawl, the number of links grabbed (that were unique on a per-page basis)
    """
    crawl_length = 0
    grabbed_links.append(Link(input_url, "http://www.rivergillis.com/"))
    while grabbed_links:
        crawl()
        crawl_length += 1
        print("crawl length is now", crawl_length)

    return crawl_length


def crawl():
    """
    pops off the top link from grabbed_links, makes a page for it, updates the page counts and extends grabbed_links
    :return: length of the crawl
    """
    if not grabbed_links:
        return
    current_link = grabbed_links.pop()

    if current_link in has_grabbed:
        # If we've already grabbed this link before, increment the corresponding page and return
        page_to_increment = pages_by_links[current_link]
        page_counts[page_to_increment] += 1
        print("we've been to", current_link, page_counts[page_to_increment], "times now!")
        return
    else:
        has_grabbed.add(current_link)

    print("-----VISITING", current_link, "------")

    # Create a Page from the Link and connect the Link to the Page via pages_by_links
    current_page = Page(current_link.full_hyperlink)
    pages_by_links[current_link] = current_page

    # Updates the page_counts
    page_counts[current_page] = 1

    # updates the grabbed_links
    grabbed_links.extend(current_page.links)
    print("This page has", len(current_page.links), "links, we've now got", len(grabbed_links), "total links")
    return


"""
def _crawl(input_url):

    input_url: a string of a url in a fully accessible form
    Downloads the web page attached to the string and searches
    for any links contained within. Visits each web page linked
    recursively and eventually returns a list of every link found
    on that page

    
    # TODO: a valid html link begins with <!DOCTYPE html>
    # TODO: check for if we've visited https or http version (also maybe check for www or not)
    global depth
    depth += 1

    print("--------VISITING", input_url, "----------")
    print("recursion depth", depth)
    try:
        response = requests.get(input_url)
        # Note: This will be catching an SSL Error
    except IOError:
        # Attempt to visit the http instead of https site
        response = requests.get("http" + input_url[5:])

    soup = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a'))

    links = []
    for link in soup:
        if link.has_attr('href'):
            if not (link['href'].startswith("#")):
                links.append(str(link['href']))

    link_objects = {Link(link_str, input_url) for link_str in links}
    # Note: this can most likely be faster by doing a set operation on link_objects and have_visited, minus maybe?
    for link in link_objects:
        if link in have_visited:
            continue
        have_visited.add(link)
        print("found new: ", link)
        crawl(link.full_hyperlink)

    print("now returning")
    depth -= 1
    return link_objects
"""

if __name__ == "__main__":
    url = "https://reddit.com/"
    begin_crawl(url)
