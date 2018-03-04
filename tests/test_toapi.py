import pytest
from flask import request
from htmlparsing import Attr, Text
from webtest import TestApp as App

from toapi import Item, Api
from toapi.cli import cli


def test_api():
    api = Api()

    @api.site('https://news.ycombinator.com')
    @api.list('.athing')
    @api.route('/posts?page={page}', '/news?p={page}')
    @api.route('/posts', '/news?p=1')
    class Post(Item):
        url = Attr('.storylink', 'href')
        title = Text('.storylink')

    @api.site('https://news.ycombinator.com')
    @api.route('/posts?page={page}', '/news?p={page}')
    @api.route('/posts', '/news?p=1')
    class Page(Item):
        next_page = Attr('.morelink', 'href')

        def clean_next_page(self, value):
            return api.convert_string('/' + value, '/news?p={page}', request.host_url.strip('/') + '/posts?page={page}')

    app = App(api.app)
    with pytest.raises(SystemExit):
        api.run(port=-1)
    app.get('/posts?page=1')
    app.get('/posts?page=1')
    print(cli.__dict__)


def test_error():
    api = Api()

    @api.site('https://news.ycombinator.com')
    @api.list('.athing')
    @api.route('/posts?page={page}', '/news?p={page}')
    @api.route('/posts', '/news?p=1')
    class Post(Item):
        url = Attr('.storylink', 'no this attribute')
        title = Text('.storylink')

    app = App(api.app)
    with pytest.raises(Exception):
        app.get('/posts?page=1')
