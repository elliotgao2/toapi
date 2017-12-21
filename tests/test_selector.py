#!/usr/bin/env python
from lxml import etree

from toapi import Css, XPath, Regex

HTML = """
<html>
    <head>
        <title>toapi</title>
    </head>
    <body>
        <p>
            <a class="test_link" href="https://github.com/gaojiuli/toapi">hello toapi.</a>
        </p>
        <div class="block">
            <p class="p1">
                hello, P1<br/>
                this is new line
            </p>
            <p class="p2">
                <span>this is a line</span>
                <a href="#">this is a link</a>
            </p>
        </div>
    </body>
</html>
"""

html = etree.HTML(HTML)


def test_css():
    field = Css(rule="head title", attr=None)
    inline_field = Css(rule="p.p1", attr='html')
    value = field.parse(html)
    inline_field_value = inline_field.parse(html)
    assert isinstance(inline_field_value, list) == True
    assert value == "toapi"


def test_css_attr():
    field = Css(rule="p a.test_link", attr='href')
    value = field.parse(html)
    assert value == "https://github.com/gaojiuli/toapi"


def test_xpath():
    field = XPath(rule="/html/head/title/text()")
    value = field.parse(html)
    assert value == "toapi"


def test_regex():
    field = Regex(rule=r'<title>(.*?)</title>')
    value = field.parse(html)
    assert value[0] == "toapi"
