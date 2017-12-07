#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
store the html content and url
"""

import time
import hashlib
import os
import records
from datetime import datetime


class DiskStore:

    """
    DiskStore will create a hidden file --html at local path
    You can give a path like: "/Users/toapi/" or "/Users/toapi"
    then the hidden file --html will created in given path "/User/toapi/.html"
    file name is a hash of url
    about get function:
    you can give 3 params: url, default and expiration
    url: the source url you want to request
    default: return to you the default if instance can not find url source stored in disk
    expiration: means that you do not need source stored over expiration 
    """

    path = os.getcwd()

    def __init__(self, path='./'):

        try:
            os.listdir(path)
        except Exception as e:
            raise TypeError("Please input correct path")

        if path.endswith("/"):
            if not os.path.exists(path + ".html"):
                os.mkdir(path + ".html")
            self.path = path + ".html/"
        else:
            if not os.path.exists(path + "/.html"):
                os.mkdir(path + "/.html")
            self.path = path + "/.html/"

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        with open(self.path + file_name, "wb") as f:
            f.write(html.encode())
        return True

    def get(self, url, default=None, expiration="inf"):

        file_name = hashlib.md5(url.encode()).hexdigest()
        file_path = self.path + file_name

        try:
            # file change date
            change_date = os.stat(file_path).st_ctime
            if (time.time() - change_date) > float(expiration):
                # delete file
                os.remove(file_path)
                return default

            with open(file_path, "rb") as f:
                data = f.read()
            return data
        except FileNotFoundError as e:
            return default


class DBStore:

    """
    about storage, storage is a dict including keys DB_URL and NAME
    support database: mysql, postgresql, sqlite, oracle e.t.
    Mysql:
    storage = {
        "DB_URL": "mysql://name:password@host/dbname",
    }
    and so on

    about get function:
    you can give 3 params: url, default and expiration
    url: the source url you want to request
    default: return to you the default if instance can not find url source stored in disk
    expiration: means that you do not need source stored over expiration
    """

    def __init__(self, storage: dict):

        db_url = storage.get("DB_URL")
        self.db = records.Database(db_url)
        self.db.query("""CREATE TABLE IF NOT EXISTS `ToApi`(`url` VARCHAR(100),
                         `html` MEDIUMTEXT NOT NULL,`create_time` DATETIME NOT NULL,PRIMARY KEY ( `url` ))
                         ENGINE=InnoDB DEFAULT CHARSET=utf8;""")

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        html_store = html.replace("'", "toapi%%%###$$$***toapi")
        row = self.db.query("SELECT html FROM ToApi where url='{}';".format(file_name)).first()

        if row:
            self.db.query("UPDATE ToApi SET html='{}', create_time='{}' WHERE url='{}';".format(
                html_store, datetime.now(), url))
            return True
        else:
            self.db.query("INSERT INTO ToApi (url, html, create_time) VALUES ('{}', '{}', '{}');".format(
                file_name, html_store, datetime.now()))
            return True

    def get(self, url, default=None, expiration="inf"):

        file_name = hashlib.md5(url.encode()).hexdigest()
        row = self.db.query("SELECT html, create_time FROM ToApi where url='{}';".format(file_name)).first()

        try:
            create_time = dict(row).get("create_time")
            if (datetime.now()-create_time).total_seconds() > float(expiration):
                self.db.query("DELETE FROM ToApi WHERE url='{}';".format(file_name))
                return default
            origin_data = dict(row).get("html")
            data = origin_data.replace("toapi%%%###$$$***toapi", "'")
        except TypeError as e:
            return default
        return data
