from bs4 import BeautifulSoup, SoupStrainer
from link import Link
import requests

# TODO: cover all cases where a url is empty
# TODO: create unit testing for these functions
# TODO: create a link data type that specifies form and other things
# TODO: this data can be serialized onto the disc using pickle
# TODO: Fix for http://miniorange.com/fraud/


def move_up_dirs(link, root_url):
    """
    :param link: a link of url with an arbitrary number of dirs to traverse (ex: './../././../test')
    :param root_url: a link of the root url from which link was linked
    :return:
    """
    pass

have_visited = set()


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
        all_links(link.full_hyperlink)

    print("now returning")
    return link_objects

if __name__ == "__main__":
    url = "https://www.reddit.com/"
    all_links(url)
