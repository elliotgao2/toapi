from collections import defaultdict

import requests
from flask import Flask, logging, request, jsonify
from htmlparsing import HTMLParsing
from parse import parse

from .item import Item


class Api:

    def __init__(self, site: str = '') -> None:
        self.app: Flask = None
        self._site = site.strip('/')
        self._routes: list = []
        self._cache = defaultdict(dict)
        self._storage = defaultdict(str)
        self.__init_server()

    def __init_server(self) -> None:
        self.app = Flask(__name__)
        self.app.logger.setLevel(logging.ERROR)

        @self.app.route('/<path:path>')
        def handler(path):
            full_path = request.full_path.strip('?')
            results = self.parse_url(full_path)
            return jsonify(results)

    def absolute_url(self, base_url, url: str) -> str:
        return '{}/{}'.format(base_url, url.lstrip('/'))

    def parse_url(self, full_path: str) -> dict:
        results = self._cache.get(full_path)
        if results is not None:
            return results

        results = {}
        for url, target_url, item in self._routes:
            parsed_words = parse(url, full_path)
            if parsed_words is not None:
                parsed_path = target_url.format(**parsed_words.named)
                full_url = self.absolute_url(item._site, parsed_path)
                html = self.fetch(full_url)
                result = self.parse_html(html, item)
                results.update({item.__name__: result})

        self._cache[full_path] = results
        return results

    def parse_html(self, html: str, item: Item):
        if item._list:
            result = HTMLParsing(html).list(item._selector, item.__fields__)
        else:
            result = HTMLParsing(html).detail(item.__fields__)
        return result

    def fetch(self, url: str) -> str:
        html = self._storage.get(url)
        if html is not None:
            return html

        r = requests.get(url)
        r.encoding = None
        self._storage[url] = r.text
        return r.text

    def route(self, url: str, target_url: str) -> callable:

        def fn(item):
            self._routes.append([url, target_url, item])
            return item

        return fn

    def list(self, selector: str) -> callable:

        def fn(item):
            item._list = True
            item._selector = selector
            return item

        return fn

    def site(self, site: str) -> callable:

        def fn(item):
            item._site = site or self._site
            item._site = item._site.strip('/')
            return item

        return fn
