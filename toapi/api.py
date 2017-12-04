import re

import requests
from selenium import webdriver


class Api:
    """Api handle the routes dispatch"""

    def __init__(self, base_url, with_ajax=False, *args, **kwargs):
        self.base_url = base_url
        self.with_ajax = with_ajax
        self.items = []
        if with_ajax:
            self._browser = webdriver.PhantomJS()

    def parse(self, url):
        """Parse items from a url"""
        items = []
        for index, item in enumerate(self.items):
            if re.match(item['regex'], url):
                items.append(item['item'])
        if len(items) > 0:
            html = self._fetch_page_source(self.base_url + url)
            return self._parse_items(html, *items)
        else:
            return None

    def register(self, item):
        """Register route"""
        self.items.append({
            'regex': item.Meta.route,
            'item': item
        })

    def serve(self, ip='0.0.0.0', post='5000'):
        """Serve as an api server powered by flask"""
        from flask import Flask, jsonify, request
        app = Flask(__name__)

        @app.errorhandler(404)
        def page_not_found(error):
            try:
                return jsonify(self.parse(request.path))
            except Exception as e:
                return str(e)

        app.run(ip, post)

    def _fetch_page_source(self, url):
        """Fetch the html of given url"""
        if self.with_ajax:
            self._browser.get(url)
            return self._browser.page_source
        return requests.get(url).text

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
