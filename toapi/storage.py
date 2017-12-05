#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
store the html content and url
"""

import os
import hashlib


class Store:

    def __init__(self, path=None):
        try:
            os.listdir(path)
        except FileNotFoundError as e:
            raise TypeError("Please input correct path")

        if path:
            if not os.path.exists(path+".html"):
                os.mkdir(path+".html")
            if path and path.endswith("/"):
                self.path = path + ".html/"
            elif path and not path.endswith("/"):
                self.path = path + "/.html/"
        else:
            if not os.path.exists(".html"):
                os.mkdir(".html")
            self.path = ".html/"

    def save(self, url, html):
        file_name = hashlib.md5(url.encode()).hexdigest()
        with open(self.path+file_name, "wb") as f:
            f.write(html.encode())
        return True

    def get(self, url):
        file_name = hashlib.md5(url.encode()).hexdigest()
        files = os.listdir(self.path)
        if file_name not in files:
            return {"status": False, "data": None}
        with open(self.path+file_name, "rb") as f:
            data = f.readlines()
        return {"status": True, "data": data}
