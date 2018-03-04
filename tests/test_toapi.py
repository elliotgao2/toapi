from toapi import Item, Api
from htmlparsing import Attr, Text


def test_api():
    api = Api()

    @api.list('.athing')
    @api.site('https://news.ycombinator.com/')
    @api.route('/posts?page={page}', '/news?p={page}')
    @api.route('/posts', '/news?p=1')
    class Post(Item):
        url = Attr('.storylink', 'href')
        title = Text('.storylink')

    @api.site('https://news.ycombinator.com/')
    @api.route('/posts?page={page}', '/news?p={page}')
    @api.route('/posts', '/news?p=1')
    class Page(Item):
        next_page = Attr('.morelink', 'href')

    api.parse_url('/news?p=1')
