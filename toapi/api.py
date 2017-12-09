import logging
import re
import sys

import cchardet
import requests
from colorama import Fore
from selenium import webdriver

from toapi.cache import CacheSetting
from toapi.log import logger
from toapi.settings import Settings
from toapi.storage import Storage


class Api:
    """Api handle the routes dispatch"""

    def __init__(self, base_url=None, settings=None, *args, **kwargs):
        self.base_url = base_url
        self.settings = settings or Settings
        self.item_classes = []
        self.storage = Storage(settings=self.settings)
        self.cache = CacheSetting(settings=self.settings)
        if self.settings.with_ajax:
            if self.settings.headers is not None:
                for key, value in self.settings.headers.items():
                    capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
                    webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value
            phantom_options = []
            phantom_options.append('--load-images=false')
            self._browser = webdriver.PhantomJS(service_args=phantom_options)

    def parse(self, path, params=None, **kwargs):
        """Parse items from a url"""
        items = []
        for index, item in enumerate(self.item_classes):
            if path.startswith('/http'):
                full_path = path[1:]
                if item.__pattern__.match(full_path):
                    item.__url__ = full_path
                    items.append(item)
            else:
                if item.__pattern__.match(item.__base_url__ + path):
                    item.__url__ = item.__base_url__ + path
                    items.append(item)

        if len(items) < 0:
            return None

        results = {}
        pre = {}
        for item in items:
            pre[item.__url__] = pre.get(item.__url__, list())
            pre[item.__url__].append(item)

        for url, items in pre.items():
            cached_item = self.cache.get(url)
            if cached_item is not None:
                logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % url)
                results.update(cached_item)
                return results

            html = self.storage.get(url)
            if html is not None:
                logger.info(Fore.BLUE, 'Storage', 'Get<%s>' % url)
                parsed_item = self._parse_item(html, items)
            else:
                html = self._fetch_page_source(url, params=params, **kwargs)
                if self.storage.save(url, html):
                    logger.info(Fore.BLUE, 'Storage', 'Set<%s>' % url)
                parsed_item = self._parse_item(html, items)

            cached_item = self.cache.get(url) or {}
            cached_item.update(parsed_item)
            if self.cache.set(url, cached_item):
                logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % url)
            results.update(cached_item)
        return results

    def register(self, item):
        """Register route"""
        if item.__base_url__ is None:
            item.__base_url__ = self.base_url
        item.__pattern__ = re.compile(item.__base_url__ + item.Meta.route)
        self.item_classes.append(item)

    def serve(self, ip='0.0.0.0', port='5000', **options):
        """Serve as an api server"""
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        app.logger.setLevel(logging.ERROR)

        @app.route('/')
        def index():
            base_url = "{}://{}".format(request.scheme, request.host)
            basic_info = {
                "cache": "{}/{}".format(base_url, "cache"),
                "items": "{}/{}".format(base_url, "items"),
                "status": "{}/{}".format(base_url, "status"),
                "storage": "{}/{}".format(base_url, "storage")
            }
            return jsonify(basic_info)

        @app.route('/items/')
        def info():
            res = {
                item.__name__: "{}://{}/{}".format(request.scheme, request.host, item.__base_url__ + item.Meta.route)
                for item in self.item_classes
            }
            logger.info(Fore.GREEN, 'Received', '%s %s 200' % (request.url, len(res)))
            return jsonify(res)

        @app.errorhandler(404)
        def page_not_found(error):
            path = request.full_path
            if path.endswith('?'):
                path = path[:-1]
            try:
                result = self.cache.get(path)
                if result is not None:
                    logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % path)
                else:
                    result = self.parse(path)
                    if result is not None and self.cache.set(path, result):
                        logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % path)
                    else:
                        logger.error('Received', '%s 404' % request.url)
                        return 'Not Found', 404

                res = jsonify(result)
                logger.info(Fore.GREEN, 'Received', '%s %s 200' % (request.url, len(res.response)))
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
        if self.settings.with_ajax:
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

    def _parse_item(self, html, items):
        """Parse kinds of items from html"""
        result = {}
        for item in items:
            result[item.__name__] = item.parse(html)
            if len(result[item.__name__]) == 0:
                logger.error('Parsed', 'Item<%s[%s]>' % (item.__name__.title(), len(result[item.__name__])))
            else:
                logger.info(Fore.CYAN, 'Parsed', 'Item<%s[%s]>' % (item.__name__.title(), len(result[item.__name__])))
        return result
