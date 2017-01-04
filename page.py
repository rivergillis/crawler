from bs4 import BeautifulSoup, SoupStrainer
from link import Link
import requests


class Page(object):

    def __init__(self, full_hyperlink, links=None):
        self.full_hyperlink = full_hyperlink
        self.links = links

        # This doesn't feel great, maybe pull root_url creation method out of Link?
        self.domain = Link("#null", self.full_hyperlink).root_url

    def get_full_hyperlink(self):
        return self.full_hyperlink

    def get_links(self):
        if not self.links:
            self.create_links()
        return self.links

    def create_links(self):
        """
        this method creates a set of links by downloading the html and searching for link tags
        :return: a set of Link objects
        """
        try:
            response = requests.get(self.full_hyperlink)
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

        self.links = {Link(link_str, self.full_hyperlink) for link_str in links if not link_str.startswith("mailto:")}

    def __str__(self):
        links_buffer = ""
        if self.links:
            for link in self.links:
                links_buffer += link.full_hyperlink + "\n"
        return "Page at " + self.full_hyperlink + " with links:\n" + links_buffer
