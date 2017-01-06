from bs4 import BeautifulSoup, SoupStrainer
from link import Link
import requests


class Page(object):

    def __init__(self, full_hyperlink, links=None):
        self.full_hyperlink = full_hyperlink
        self.links = links

        if not self.links:
            self.create_links()

        # This doesn't feel great, maybe pull root_url creation method out of Link?
        self.domain = Link("#null", self.full_hyperlink).root_url

    def get_full_hyperlink(self):
        return self.full_hyperlink

    def get_links(self):
        # This could possibly become slow for large pages with no links
        return self.links

    def create_links(self):
        """
        this method creates a set of links by downloading the html and searching for link tags
        :return: a set of Link objects
        """
        try:
            response = requests.get(self.full_hyperlink, timeout=1)
        except requests.exceptions.Timeout:
            print("Page at", self.full_hyperlink, "has timed out!")
            return  # Note: self.links will now be None (causing the hash to be the same for all None'd pages)

            # Note: This will be catching an SSL Error
        except IOError:
            # Attempt to visit the http instead of https site
            response = requests.get("http" + self.full_hyperlink[5:])

        soup = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a'))

        links = []
        for link in soup:
            if link.has_attr('href'):
                if not (link['href'].startswith("#")):
                    links.append(str(link['href']))

        # needs to be a frozenset so that we can hash a Page using these links
        nonfrozen = {Link(link_str, self.full_hyperlink) for link_str in links if not link_str.startswith("mailto:")
                     and not "?" in link_str}
        self.links = frozenset(nonfrozen)

    def __str__(self):
        links_buffer = ""
        if self.links:
            for link in self.links:
                links_buffer += link.full_hyperlink + "\n"
        return "Page at " + self.full_hyperlink + " with links:\n" + links_buffer

    def __hash__(self):
        return hash(self.links)

    def __eq__(self, other):
        return self.links == other.links

    def __ne__(self, other):
        return not(self.links == other.links)