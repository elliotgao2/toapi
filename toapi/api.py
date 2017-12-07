import logging
import re
import sys

import cchardet
import requests
from colorama import Fore
from selenium import webdriver

from toapi.cache import MemoryCache
from toapi.log import logger
from toapi.storage import DiskStore

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Api:
    """Api handle the routes dispatch"""

    def __init__(self, base_url, with_ajax=False, *args, **kwargs):
        self.base_url = base_url
        self.with_ajax = with_ajax
        self.items = []
        self.cache = MemoryCache()
        self.storage = DiskStore()
        if with_ajax:
            phantom_options = []
            phantom_options.append('--load-images=false')
            self._browser = webdriver.PhantomJS(service_args=phantom_options)

    def parse(self, url, params=None, **kwargs):
        """Parse items from a url"""

        items = self.cache.get(url)
        if items is not None:
            logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % url)
            return items

        items = []
        for index, item in enumerate(self.items):
            if re.compile(item['regex']).match(url):
                items.append(item['item'])

        if len(items) > 0:
            html = self.storage.get(url)
            if html is not None:
                logger.info(Fore.BLUE, 'Storage', 'Get<%s>' % url)
                items = self._parse_items(html, *items)
            else:
                html = self._fetch_page_source(self.base_url + url, params=params, **kwargs)
                if self.storage.save(url, html):
                    logger.info(Fore.BLUE, 'Storage', 'Set<%s>' % url)
                items = self._parse_items(html, *items)
            if self.cache.set(url, items):
                logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % url)
            return items
        else:
            return None

    def register(self, item):
        """Register route"""
        self.items.append({
            'regex': item.Meta.route,
            'item': item
        })

    def serve(self, ip='0.0.0.0', port='5000', debug=None, **options):
        """Todo: Serve as an api server powered by flask"""
        from flask import Flask, jsonify, request
        app = Flask(__name__)
        app.debug = True
        app.logger.setLevel(logging.ERROR)

        @app.errorhandler(404)
        def page_not_found(error):
            parse_result = urlparse(request.url)
            if parse_result.query != '':
                url = '{}?{}'.format(
                    parse_result.path,
                    parse_result.query
                )
            else:
                url = request.path
            try:
                res = jsonify(self.parse(url))
                logger.info(Fore.GREEN, 'Received', '%s %s' % (request.url, len(res.response[0])))
                return res
            except Exception as e:
                return str(e)

        logger.info(Fore.WHITE, 'Serving', 'http://%s:%s' % (ip, port))
        try:
            app.run(ip, port, debug=False, **options)
        except KeyboardInterrupt:
            sys.exit()

    def _fetch_page_source(self, url, params=None, **kwargs):
        """Fetch the html of given url"""
        if self.with_ajax:
            self._browser.get(url)
            text = self._browser.page_source
            if text != '':
                logger.info(Fore.GREEN, 'Sent', '%s %s 200' % (url, len(text)))
            else:
                logger.error('Sent', '%s %s' % (url, len(text)))
            return text
        else:
            response = requests.get(url, params=params, **kwargs)
            content = response.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            if response.status_code != 200:
                logger.error('Sent', '%s %s %s' % (url, len(text), response.status_code))
            else:
                logger.info(Fore.GREEN, 'Sent', '%s %s %s' % (url, len(text), response.status_code))
            return text

    def _parse_item(self, html, item):
        """Parse a single item from html"""
        result = {}
        result[item.name] = item.parse(html)
        if len(result[item.name]) == 0:
            logger.error('Parsed', 'Item<%s[%s]>' % (item.name.title(), len(result[item.name])))
        else:
            logger.info(Fore.CYAN, 'Parsed', 'Item<%s[%s]>' % (item.name.title(), len(result[item.name])))
        return result

    def _parse_items(self, html, *items):
        """Parse kinds of items from html"""
        results = {}
        for item in items:
            results.update(self._parse_item(html, item))
        return results
