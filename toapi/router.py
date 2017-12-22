#!/usr/bin/env python
import re

from collections import defaultdict, OrderedDict


class Router:
    """
    Router supports basic routing with Items checks
    """

    def __init__(self):
        self.routes = defaultdict(list)
        self.alias_map = {}
        self.routes_map = {}

    def add_route(self, item):
        """
        Adds a item to the routes dict
        :return:
        """
        route_dict = OrderedDict(item.Meta.route)
        for item_alias, item_route in route_dict.items():
            _alias_re = self.get_alias_re(alias=item_alias)
            self.routes[_alias_re].append(item)
            self.routes_map[_alias_re] = item_route

    def get_items(self, path):
        """
        Get items
        :param path: source path
        :return: all_items
        """
        all_items = {}
        for alias_re, items in self.routes.items():
            converted_path = self.convert_route_to_alias(path, alias_re, self.routes_map[alias_re])
            if converted_path:
                all_items[converted_path] = items
        return all_items

    def get_alias_re(self, alias):
        alias = '^' + alias.replace('?', '\?') + '$'
        _alias_re = self.alias_map.get(alias, None)
        if _alias_re is None:
            _alias_re_string = re.sub(':(?P<params>[a-z_]+)',
                                      lambda m: '(?P<{}>[A-Za-z0-9_?&/=\s\-\u4e00-\u9fa5]+)'.format(m.group('params')),
                                      alias)
            _alias_re = re.compile(_alias_re_string)
            self.alias_map[alias] = _alias_re
        return _alias_re

    def convert_route_to_alias(self, path, alias_re, route):
        """Convert alias to route

        Example:
            $ convert_route_to_alias('/movies/?page=2', '/movies/?page=:page', '/html/gndy/dyzz/index_:page.html')
            >> /html/gndy/dyzz/index_2.html

        Args:
            path (str): source path.
            alias (str): source path expression.
            route (str): destination path expression.

        Returns:
            str: The covert result
        """
        matched = alias_re.match(path)
        if not matched:
            return False
        result_dict = matched.groupdict()
        try:
            result = re.sub(':(?P<params>[a-z_]+)',
                            lambda m: '{}'.format(result_dict.get(m.group('params'))),
                            route)
        except Exception:
            return False
        return result
