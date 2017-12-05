#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
store the html content and url
"""

import os
import hashlib


class Store:

    def __init__(self):
        if not os.path.exists(".html"):
            os.mkdir(".html")

    def save(self, url, html):
        pass

    def get(self, url):
        pass


