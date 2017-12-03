import re

import requests


class Api:
    """Api handle the routes dispatch"""

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        self.items = []

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

    def serve(self, ip, post):
        """Todo: Serve as an api server powered by flask"""
        pass

    def _fetch_page_source(self, url):
        """Fetch the html of given url"""
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
