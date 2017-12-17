import os
import time
import hashlib

from toapi.log import logger


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
                os.makedirs(path + ".html")
            self.path = path + ".html/"
        else:
            if not os.path.exists(path + "/.html"):
                os.makedirs(path + "/.html")
            self.path = path + "/.html/"

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.path + file_name, "w", encoding="utf-8") as f:
            f.write(html)
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

            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            return data
        except FileNotFoundError as e:
            return default
