import requests
from flask import Flask, logging, request, jsonify
from htmlparsing import HTMLParsing
from parse import parse

from .item import Item


class Api:

    def __init__(self, base_url: str = ''):
        self.base_url = base_url.strip('/')
        self.routes: list = []
        self.app: Flask = None
        self.__init_server()

    def __init_server(self):
        self.app = Flask(__name__)
        self.app.logger.setLevel(logging.ERROR)

        @self.app.route('/<path:path>')
        def handler(path):
            results = {}
            fetched_url = {}
            full_path = request.full_path.strip('?')
            for url, target_url, item in self.routes:
                parsed_words = parse(url, full_path)
                if parsed_words is not None:
                    fetching_url = target_url.format(**parsed_words.named)
                    base_url = item._base_url or self.base_url
                    full_fetching_url = self.absolute_url(base_url, fetching_url)
                    html = fetched_url.get(full_fetching_url) or self.fetch(full_fetching_url)
                    result = self.parse(html, item)
                    results.update({item.__name__: result})
            return jsonify(results)

    def absolute_url(self, base_url, url: str) -> str:
        return '{}/{}'.format(base_url, url.lstrip('/'))

    def parse(self, html: str, item: Item):
        if item._list:
            result = HTMLParsing(html).list(item._selector, item.__fields__)
        else:
            result = HTMLParsing(html).detail(item.__fields__)
        return result

    def fetch(self, url: str) -> str:
        r = requests.get(url)
        r.encoding = None
        return r.text

    def route(self, url: str, target_url: str) -> callable:

        def fn(item):
            self.routes.append([url, target_url, item])
            return item

        return fn

    def list(self, selector: str) -> callable:

        def fn(item):
            item._list = True
            item._selector = selector
            return item

        return fn

    def site(self, base_url: str) -> callable:

        def fn(item):
            item._base_url = base_url.strip('/')
            return item

        return fn
