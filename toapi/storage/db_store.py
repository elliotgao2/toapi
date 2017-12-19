import hashlib
from time import time

from sqlalchemy import create_engine


class DBStore:
    """
    about storage, storage is a dict including keys DB_URL and NAME
    support database: mysql, postgresql, sqlite, oracle e.t.
    Mysql:
        db_url: "mysql://name:password@host/dbname",
    and so on

    about get function:
    you can give 3 params: url, default and expiration
    url: the source url you want to request
    default: return to you the default if instance can not find url source stored in disk
    expiration: means that you do not need source stored over expiration
    """
    MYSQL_SQL = """CREATE TABLE IF NOT EXISTS `ToApi`(
                   `url` VARCHAR(100),
                   `html` MEDIUMTEXT NOT NULL,
                   `create_time` FLOAT NOT NULL,
                   PRIMARY KEY ( `url` )) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;"""
    SQLITE_SQL = """CREATE TABLE IF NOT EXISTS ToApi(
                    url VAR(100) PRIMARY KEY,
                    html TEXT,
                    create_time FLOAT);"""

    def __init__(self, db_url):

        self.db = create_engine(db_url)
        if db_url.startswith("mysql"):
            self.db.execute(self.MYSQL_SQL)
        elif db_url.startswith("sqlite"):
            self.db.execute(self.SQLITE_SQL)
        else:
            self.db.execute(self.MYSQL_SQL)

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        html_store = html.replace("\"", "toapi###$$$###toapi")
        html_store = html_store.replace("\'", "toapi***$$$***toapi").encode("unicode-escape")
        sql = """SELECT html 
                 FROM ToApi
                 WHERE url="{}";""".format(file_name)
        row = self.db.execute(sql).first()
        if row:
            sql = """UPDATE ToApi 
                     SET html="{}", create_time="{}" 
                     WHERE url="{}";""".format(html_store, time(), file_name)
            self.db.execute(sql)
            return True
        else:
            self.db.execute("""INSERT INTO ToApi (url, html, create_time) VALUES ("{}", "{}", "{}");""".format(
                file_name, html_store, time()))
            return True

    def get(self, url, default=None, expiration="inf"):

        file_name = hashlib.md5(url.encode()).hexdigest()
        row = self.db.execute("SELECT html, create_time FROM ToApi where url='{}';".format(file_name)).first()
        try:
            origin_data = dict(row).get("html")
            create_time = dict(row).get("create_time")
            if (time() - create_time) > float(expiration):
                self.db.execute("DELETE FROM ToApi WHERE url='{}';".format(file_name))
                return default
            data = eval(origin_data).decode("unicode-escape")
            data = data.replace("toapi###$$$###toapi", "\"").replace("toapi***$$$***toapi", "\'")
        except TypeError as e:
            return default
        return data
