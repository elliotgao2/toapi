import re

import cchardet
import requests
from colorama import Fore
from selenium import webdriver

from toapi.cache import CacheSetting
from toapi.log import logger
from toapi.server import Server
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
        self.server = Server(self, settings=self.settings)
        self.browser = self.get_browser(settings=self.settings)

    def get_browser(self, settings):
        if settings.headers is not None:
            for key, value in settings.headers.items():
                capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
                webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value
        phantom_options = []
        phantom_options.append('--load-images=false')
        return webdriver.PhantomJS(service_args=phantom_options)

    def parse(self, path, params=None, **kwargs):
        """Parse items from a url"""

        items = {}
        for index, item in enumerate(self.item_classes):
            full_path = path[1:] if path.startswith('/http') else item.__base_url__ + path
            if item.__pattern__.match(full_path):
                items[full_path] = items.get(full_path, list())
                items[full_path].append(item)

        results = {}
        for url, items in items.items():
            cached_item = self.get_cache(url)
            if cached_item is not None:
                results.update(cached_item)
            else:
                html = self.get_storage(url) or self.fetch_page_source(url, params=params, **kwargs)
                if html is not None:
                    parsed_item = self.parse_item(html, items)
                    results.update(parsed_item)
                    self.set_cache(url, parsed_item)
        return results or None

    def register(self, item):
        """Register items"""
        item.__base_url__ = item.__base_url__ or self.base_url
        item.__pattern__ = re.compile(item.__base_url__ + item.Meta.route)
        self.item_classes.append(item)

    def serve(self, ip='0.0.0.0', port='5000', **options):
        self.server.serve(ip, port, **options)

    def fetch_page_source(self, url, params=None, **kwargs):
        """Fetch the html of given url"""
        self.update_status('_status_sent')
        if self.settings.with_ajax:
            self.browser.get(url)
            text = self.browser.page_source
            if text != '':
                logger.info(Fore.GREEN, 'Sent', '%s %s 200' % (url, len(text)))
            else:
                logger.error('Sent', '%s %s' % (url, len(text)))
            result = text
        else:
            response = requests.get(url, params=params, **kwargs)
            content = response.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            if response.status_code != 200:
                logger.error('Sent', '%s %s %s' % (url, len(text), response.status_code))
            else:
                logger.info(Fore.GREEN, 'Sent', '%s %s %s' % (url, len(text), response.status_code))
            result = text
        self.set_storage(url, result)
        return result

    def update_status(self, key):
        """Set cache"""
        self.cache.set(key, str(self.get_status(key) + 1))

    def get_status(self, key):
        if self.cache.get(key) is None:
            self.cache.set(key, '0')
        return int(self.cache.get(key))

    def set_cache(self, key, value):
        """Set cache"""
        if self.cache.get(key) is None and self.cache.set(key, value):
            logger.info(Fore.YELLOW, 'Cache', 'Set<%s>' % key)
            self.update_status('_status_cache_set')
            return True
        return False

    def get_cache(self, key, default=None):
        """Set cache"""
        result = self.cache.get(key)
        if result is not None:
            logger.info(Fore.YELLOW, 'Cache', 'Get<%s>' % key)
            self.update_status('_status_cache_get')
            return result
        return default

    def set_storage(self, key, value):
        """Set storage"""
        if self.storage.get(key) is None and self.storage.save(key, value):
            logger.info(Fore.BLUE, 'Storage', 'Set<%s>' % key)
            self.update_status('_status_storage_set')
            return True
        return False

    def get_storage(self, key, default=None):
        """Set storage"""
        result = self.storage.get(key)
        if result is not None:
            logger.info(Fore.BLUE, 'Storage', 'Get<%s>' % key)
            self.update_status('_status_storage_get')
            return result
        return default

    def parse_item(self, html, items):
        """Parse kinds of items from html"""
        result = {}
        for item in items:
            result[item.__name__] = item.parse(html)
            if len(result[item.__name__]) == 0:
                logger.error('Parsed', 'Item<%s[%s]>' % (item.__name__.title(), len(result[item.__name__])))
            else:
                logger.info(Fore.CYAN, 'Parsed', 'Item<%s[%s]>' % (item.__name__.title(), len(result[item.__name__])))
        return result
