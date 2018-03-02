import requests
from flask import Flask, logging, request
from parse import parse


class Api:

    def __init__(self, base_url: str):
        self.base_url = base_url.strip('/')
        self.app: Flask = None
        self.url_map = []
        self.__init_server()

    def __init_server(self):
        self.app = Flask(__name__)
        self.app.logger.setLevel(logging.ERROR)

        @self.app.route('/<path:path>')
        def handler(path):
            print(self.url_map)
            for url, target_url, item in self.url_map:
                parsed_words = parse(url, request.full_path)
                if parsed_words:
                    target_url = target_url.format(**parsed_words.named)
                    return self.fetch(self.absolute_url(target_url))
            return 'Not Found'

    def absolute_url(self, url: str):
        return '{}/{}'.format(self.base_url, url.lstrip('/'))

    def fetch(self, url):
        r = requests.get(url)
        r.encoding = None
        return r.text

    def route(self, url_map: list):
        def fn(item):
            url_map.append(item)
            self.url_map.append(url_map)
            return item

        return fn

    def list(self, selector: str):
        def fn(item):
            item.__selector = selector
            return item

        return fn
