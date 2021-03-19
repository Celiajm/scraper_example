import urllib3
import re
from bs4 import BeautifulSoup


class soup_base:

    MATCH_ALL = r".*"

    def __init__(self, url):
        soup = BeautifulSoup(url, "lxml")
        self.soup = soup

    def get_soup(url, header):
        return BeautifulSoup(urllib3.urlopen(urllib3.Request(url, headers=header)), "html.parser")

    def find_specific_with_text(self, type, string):
        specifics = self.soup.find(type, text=string)
        return specifics

    def find_specific(self, type, extra):
        specifics = self.soup.findAll(type, extra)
        return specifics

    def find_next(self, element, next):
        return element.find_next(next)

    def find_all_specific(self, type, subType, value):
        values = self.soup.findAll(type, {subType: value})
        return values

    def find_all_generic(self, type):
        values = self.soup.findAll(type)
        return values

    def like(self, string):
        """
        Return a compiled regular expression that matches the given
        string with any prefix and postfix, e.g. if string = "hello",
        the returned regex matches r".*hello.*"
        """
        string_ = string
        if not isinstance(string_, str):
            string_ = str(string_)
        regex = self.MATCH_ALL + re.escape(string_) + self.MATCH_ALL
        return re.compile(regex, flags=re.DOTALL)

    def find_by_next_by_text(self, text, tag, subtag, value, next, multiple=False):
        """
        Find the tag in soup that matches all provided kwargs, and contains the
        text.

        If no match is found, return None.
        If more than one match is found, raise ValueError.
        """
        elements = self.soup.find_all(tag, {subtag: value})
        matches = []
        for element in elements:
            if element.find(text=self.like(text)):
                matches.append(element)
        if multiple:
            return matches
        if len(matches) == 0:
            return None
        else:
            return matches[0].find_next(next).text

    def find_by_text(self, text, tag, subtag, value, multiple=False):
        """
        Find the tag in soup that matches all provided kwargs, and contains the
        text.

        If no match is found, return None.
        If more than one match is found, raise ValueError.
        """
        elements = self.soup.find_all(tag, {subtag: value})
        matches = []
        for element in elements:
            if element.find(text=self.like(text)):
                matches.append(element)
        if multiple:
            return matches
        if len(matches) == 0:
            return None
        else:
            return matches[0]

    def find_by_text_generic(self, text, tag, multiple=False):
        """
        Find the tag in soup that matches all provided kwargs, and contains the
        text.

        If no match is found, return None.
        If more than one match is found, raise ValueError.
        """
        elements = self.soup.find_all(tag)
        matches = []
        for element in elements:
            if element.find(text=self.like(text)):
                matches.append(element)
        if multiple:
            return matches
        if len(matches) == 0:
            return None
        else:
            return matches[0]
