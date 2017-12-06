#!/usr/bin/env python
from lxml import etree

from toapi import Css, XPath

HTML = """
<html>
    <head>
        <title>toapi</title>
    </head>
    <body>
        <p>
            <a class="test_link" href="https://github.com/gaojiuli/toapi">hello toapi.</a>
        </p>
    </body>
</html>
"""

html = etree.HTML(HTML)


def test_css():
    field = Css(rule="head title", attr=None)
    value = field.parse(html)
    assert value == "toapi"


def test_css_attr():
    field = Css(rule="p a.test_link", attr='href')
    value = field.parse(html)
    assert value == "https://github.com/gaojiuli/toapi"


def test_xpath():
    field = XPath(rule="/html/head/title/text()")
    value = field.parse(html)
    assert value == "toapi"
