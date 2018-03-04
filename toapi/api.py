import traceback
from collections import defaultdict

import cchardet
import requests
from colorama import Fore
from flask import Flask, logging, request, jsonify
from parse import parse

from toapi.log import logger


class Api:

    def __init__(self, site: str = '') -> None:
        self.app: Flask = Flask(__name__)
        self._site = site.strip('/')
        self._routes: list = []
        self._cache = defaultdict(dict)
        self._storage = defaultdict(str)
        self.__init_server()

    def __init_server(self) -> None:
        self.app.logger.setLevel(logging.ERROR)

        @self.app.route('/<path:path>')
        def handler(path):
            logger.info(Fore.GREEN, 'Received', f'{request.url}')

            try:
                full_path = request.full_path.strip('?')
                results = self.parse_url(full_path)
                return jsonify(results)
            except Exception as e:
                logger.error('Serving', f'{e}')
                print(traceback.print_exc())
                return jsonify({'msg': 'System Error', 'code': -1}), 500

    def run(self, host='127.0.0.1', port=5000, **options):
        try:
            logger.info(Fore.GREEN, 'Serving', f'http://{host}:{port}')
            self.app.run(host, port, **options)
        except Exception as e:
            logger.error('Serving', '%s' % str(e))
            print(traceback.print_exc())
            exit()

    def absolute_url(self, base_url, url: str) -> str:
        return '{}/{}'.format(base_url, url.lstrip('/'))

    def parse_url(self, full_path: str) -> dict:
        results = self._cache.get(full_path)
        if results is not None:
            logger.info(Fore.YELLOW, 'Cache', f'Get<{full_path}>')
            return results

        results = {}
        for url, target_url, item in self._routes:
            parsed_words = parse(url, full_path)
            if parsed_words is not None:
                parsed_path = target_url.format(**parsed_words.named)
                full_url = self.absolute_url(item._site, parsed_path)
                html = self.fetch(full_url)
                result = item.parse(html)
                logger.info(Fore.CYAN, 'Parsed', f'Item<{item.__name__}[{len(result)}]>')
                results.update({item.__name__: result})

        self._cache[full_path] = results
        logger.info(Fore.YELLOW, 'Cache', f'Set<{full_path}>')

        return results

    def fetch(self, url: str) -> str:
        html = self._storage.get(url)
        if html is not None:
            logger.info(Fore.BLUE, 'Storage', f'Get<{url}>')
            return html

        r = requests.get(url)
        content = r.content
        charset = cchardet.detect(content)
        html = content.decode(charset['encoding'] or 'utf-8')
        logger.info(Fore.GREEN, 'Sent', f'{url} {len(html)} {r.status_code}')
        self._storage[url] = html
        logger.info(Fore.BLUE, 'Storage', f'Set<{url}>')
        return html

    def route(self, url: str, target_url: str) -> callable:

        def fn(item):
            self._routes.append([url, target_url, item])
            logger.info(Fore.GREEN, 'Register', f'<{item.__name__}: {url} {target_url}>')

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
