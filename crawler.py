from link import Link
from page import Page
import operator

# TODO: this data can be serialized onto the disc using pickle
# TODO: Fix for http://miniorange.com/fraud/

grabbed_links = []  # Grabbed links contains the list of upcoming Links to be crawled
has_grabbed = set()  # has_grabbed contains a set of Links that we have already grabbed
page_counts = {}   # page_counts contains the number of times a certain page has been grabbed (Page -> Count)
pages_by_links = {}  # pages_by_links has a page object for a corresponding link object (Link -> Page)


def create_log():
    logfile = open("logfile", 'w')

    sorted_counts = sorted(page_counts.items(), key=operator.itemgetter(1), reverse=True)

    for page, pcount in sorted_counts:
        logfile.write(str(page))
        logfile.write("Has been visited " + str(pcount) + " times\n\n")

    logfile.close()


def begin_crawl(input_url):
    """
    calls crawl and maintains calling it in a while loop, keeping track of the # of links grabbed
    :param input_url: the first link to begin crawling on, a string
    :return: the length of the crawl, the number of links grabbed (that were unique on a per-page basis)
    """
    crawl_length = 0
    create_log()
    grabbed_links.append(Link(input_url, "http://www.rivergillis.com/"))
    while grabbed_links:
        crawl()
        crawl_length += 1
        print("crawl length is now", crawl_length)
        if crawl_length == 200:
            create_log()
            return crawl_length

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


if __name__ == "__main__":
    url = "https://reddit.com/"
    begin_crawl(url)
