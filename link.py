"""
This is the file to be used for the link type object for crawler.py
Author: Jameson Gillis
"""
from bs4 import BeautifulSoup, SoupStrainer
from tld import get_tld
import requests
import re


class Link(object):
    """
    The Link object is to be used in crawler.py to handle all types of links obtained while searching html
    Links have:
        raw_value: a string representing the input value that the Link was created with
        raw_base: a string representing the web page that the raw_value was found on
        full_hyperlink: a string value representing the completed, cleaned hyperlink to be used for accessing
    Links have many more things necessary to create the above values, those are documented by member definition
    """
    pass