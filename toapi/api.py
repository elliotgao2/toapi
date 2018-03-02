import requests
from flask import Flask, logging, request, jsonify
from htmlparsing import HTMLParsing
from parse import parse


class Api:

    def __init__(self, base_url: str):
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
            for url, target_url, item in self.routes:
                parsed_words = parse(url, request.full_path)
                if parsed_words:
                    target_url = target_url.format(**parsed_words.named)
                    html = fetched_url.get(target_url) or self.fetch(self.absolute_url(target_url))
                    if item._list:
                        result = HTMLParsing(html).list(item._selector, item.__fields__)
                    else:
                        result = HTMLParsing(html).detail(item.__fields__)
                    results.update({item.__name__: result})
            return jsonify(results)

    def absolute_url(self, url: str) -> str:
        return '{}/{}'.format(self.base_url, url.lstrip('/'))

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
