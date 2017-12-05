import re

import requests
import cchardet
from selenium import webdriver

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
        if with_ajax:
            options = []
            options.append('--load-images=false')
            self._browser = webdriver.PhantomJS(service_args=options)

    def parse(self, url, params=None, **kwargs):
        """Parse items from a url"""
        items = []
        for index, item in enumerate(self.items):
            if re.compile(item['regex']).match(url):
                items.append(item['item'])
        if len(items) > 0:
            html = self._fetch_page_source(self.base_url + url, params=params, **kwargs)
            return self._parse_items(html, *items)
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
                return jsonify(self.parse(url))
            except Exception as e:
                return str(e)

        app.run(ip, port, debug=debug, **options)

    def _fetch_page_source(self, url, params=None, **kwargs):
        """Fetch the html of given url"""

        if self.with_ajax:
            self._browser.get(url)
            return self._browser.page_source
        response = requests.get(url, params=params, **kwargs)
        content = response.content
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        return text

    def _parse_item(self, html, item):
        """Parse a single item from html"""
        result = {}
        result[item.name] = item.parse(html)
        return result

    def _parse_items(self, html, *items):
        """Parse kinds of items from html"""
        results = {}
        for item in items:
            results.update(self._parse_item(html, item))
        return results
