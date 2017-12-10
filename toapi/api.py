import logging
import re
import sys
from time import time

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

        items = {}
        for index, item in enumerate(self.item_classes):
            full_path = path[1:] if path.startswith('/http') else item.__base_url__ + path
            if item.__pattern__.match(full_path):
                items[full_path] = items.get(full_path, list())
                items[full_path].append(item)

        if len(items.keys()) <= 0:
            return None

        results = {}
        for url, items in items.items():
            cached_item = self.get_cache(url)
            if cached_item is not None:
                results.update(cached_item)

            html = self.get_storage(url) or self._fetch_page_source(url, params=params, **kwargs)
            if html is not None:
                self.set_storage(url, html)
                parsed_item = self._parse_item(html, items)
                cached_item = self.get_cache(url) or {}
                cached_item.update(parsed_item)
                self.set_cache(url, cached_item)
                results.update(cached_item)
        return results or None

    def register(self, item):
        """Register items"""
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

        @app.route('/status')
        def status():
            status = {
                'cache_set': self._get_status('_status_cache_set'),
                'cache_get': self._get_status('_status_cache_get'),
                'storage_set': self._get_status('_status_storage_set'),
                'storage_get': self._get_status('_status_storage_get'),
                'sent': self._get_status('_status_sent'),
                'received': self._get_status('_status_received')
            }
            return jsonify(status)

        @app.route('/items/')
        def items():
            result = {
                item.__name__: "{}://{}/{}".format(request.scheme, request.host, item.__base_url__ + item.Meta.route)
                for item in self.item_classes
            }
            res = jsonify(result)
            return res

        @app.errorhandler(404)
        def page_not_found(error):
            start_time = time()
            path = request.full_path
            if path.endswith('?'):
                path = path[:-1]
            try:
                result = self.get_cache(path) or self.parse(path)
                if result is None:
                    logger.error('Received', '%s 404' % request.url)
                    return 'Not Found', 404
                self.set_cache(path, result)
                res = jsonify(result)
                self._update_status('_status_received')
                end_time = time()
                time_usage = end_time - start_time
                logger.info(Fore.GREEN, 'Received', '%s %s 200 %.2fms' % (request.url, len(res.response), time_usage*1000))
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
        self._update_status('_status_sent')

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

    def _update_status(self, key):
        """Set cache"""
        self.cache.set(key, str(self._get_status(key) + 1))

    def _get_status(self, key):
        if self.cache.get(key) is None:
            self.cache.set(key, '0')
        return int(self.cache.get(key))

    def set_cache(self, key, value):
        """Set cache"""
        if self.cache.get(key) is None and self.cache.set(key, value):
            logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % key)
            self._update_status('_status_cache_set')
            return True
        return False

    def get_cache(self, key, default=None):
        """Set cache"""
        result = self.cache.get(key)
        if result is not None:
            logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % key)
            self._update_status('_status_cache_get')
            return result
        return default

    def set_storage(self, key, value):
        """Set storage"""
        if self.storage.get(key) is None and self.storage.save(key, value):
            logger.info(Fore.BLUE, 'Storage', 'Set<%s>' % key)
            self._update_status('_status_storage_set')
            return True
        return False

    def get_storage(self, key, default=None):
        """Set storage"""
        result = self.storage.get(key)
        if result is not None:
            logger.info(Fore.BLUE, 'Storage', 'Get<%s>' % key)
            self._update_status('_status_storage_get')
            return result
        return default

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
