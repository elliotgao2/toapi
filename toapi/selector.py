import re

from lxml import etree


class Selector:
    def __init__(self, rule):
        self.rule = rule

    def parse(self, html):
        """Parse string from html"""
        raise NotImplementedError()

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)


class Css(Selector):
    """Css selector"""

    def __init__(self, rule, attr):
        super().__init__(rule)
        self.attr = attr

    def parse(self, html):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        return d.cssselect(self.rule)


class XPath(Selector):
    """XPath selector"""

    def parse(self, html):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        return d.xpath(self.rule)


class Regex(Selector):
    """Regex expression"""

    def parse(self, html):
        return re.findall(self.rule, html)
