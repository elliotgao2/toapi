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

    def parse(self, html):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        value = d.cssselect(self.rule)
        if self.attr:
            # TODO
            value = value[0].get(self.attr).strip() if len(value) == 1 else value
        else:
            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], etree._Element):
                text = ''
                for node in value[0].itertext():
                    text += node.strip()
                value = text
            else:
                value = ''.join([i.text.strip() for i in value])
        return value


class XPath(Selector):
    """XPath selector"""

    def parse(self, html):
        if isinstance(html, etree._Element):
            html = etree.tostring(html)
        d = etree.HTML(html)
        value = d.xpath(self.rule)
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], etree._Element):
            text = ''
            for node in value[0].itertext():
                text += node.strip()
            value = text
        elif isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            value = ''.join(value)
        return value


class Regex(Selector):
    """Regex expression"""

    def parse(self, html):
        return re.findall(self.rule, html)
