import re

from lxml import etree


class Selector(object):
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

    def __init__(self, rule, attr=None):
        super(Css, self).__init__(rule)
        self.attr = attr

    def parse(self, html, is_source=False):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        value = d.cssselect(self.rule)
        if is_source:
            return value
        if self.attr:
            value = value[0].get(self.attr, value) if len(value) == 1 else value
        else:
            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], etree._Element):
                text = ''
                for node in value[0].itertext():
                    text += node
                value = text
        return value


class XPath(Selector):
    """XPath selector"""

    def parse(self, html, is_source=False):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        value = d.xpath(self.rule)
        if is_source:
            return value
        if isinstance(value, list) and len(value) == 1:
            if isinstance(value[0], etree._Element):
                text = ''
                for node in value[0].itertext():
                    text += node
                value = text
            if isinstance(value[0], str) or isinstance(value[0], etree._ElementUnicodeResult):
                value = ''.join(value)
        return value


class Regex(Selector):
    """Regex expression"""

    def parse(self, html):
        if isinstance(html, etree._Element):
            html = str(etree.tostring(html))
        return re.findall(self.rule, html)
