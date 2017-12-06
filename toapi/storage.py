#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
store the html content and url
"""

import os
import hashlib
import records


class DiskStore:

    path = os.getcwd()

    def __init__(self, path=path):
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
        with open(self.path+file_name, "wb") as f:
            f.write(html.encode())
        return True

    def get(self, url):
        file_name = hashlib.md5(url.encode()).hexdigest()
        try:
            with open(self.path+file_name, "rb") as f:
                data = f.readlines()
            return {"status": True, "data": data}
        except Exception as e:
            return {"status": False, "data": None}


class DBStore:

    def __init__(self, storage:dict):
        """
        about storage, storage is a dict including keys DB_URL and NAME
        support database: mysql, postgresql, sqlite, oracle e.t.
        Mysql:
        storage = {
            "DB_URL": "mysql://name:password@host/dbname",
        }
        and so on
        """

        db_url = storage.get("DB_URL")
        self.db = records.Database(db_url)
        self.db.query("""CREATE TABLE IF NOT EXISTS `ToApi`(`url` VARCHAR(100),
                         `html` MEDIUMTEXT NOT NULL,PRIMARY KEY ( `url` ))ENGINE=InnoDB DEFAULT CHARSET=utf8;""")

    def save(self, url, html):
        file_name = hashlib.md5(url.encode()).hexdigest()
        html_store = html.replace("'", "toapi%%%###$$$***toapi")
        row = self.db.query("SELECT html FROM ToApi where url='{}'".format(file_name)).first()
        if row:
            self.db.query("UPDATE ToApi SET html='{}' WHERE url='{}'".format(html_store, url))
            return True
        else:
            self.db.query("INSERT INTO ToApi (url, html) VALUES ('{}', '{}') ".format(file_name, html_store))
            return True

    def get(self, url):
        file_name = hashlib.md5(url.encode()).hexdigest()

        row = self.db.query("SELECT html FROM ToApi where url='{}'".format(file_name)).first()
        try:
            origin_data = dict(row).get("html")
            data = origin_data.replace("toapi%%%###$$$***toapi", "'")
        except TypeError as e:
            return None
        return data
