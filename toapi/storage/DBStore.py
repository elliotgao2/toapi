import records
import hashlib
from datetime import datetime


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

    def __init__(self, db_url):

        self.db = records.Database(db_url)
        self.db.query("""CREATE TABLE IF NOT EXISTS `ToApi`(`url` VARCHAR(100),
                         `html` MEDIUMTEXT NOT NULL,`create_time` DATETIME NOT NULL,PRIMARY KEY ( `url` ))
                         ENGINE=InnoDB DEFAULT character set = utf8;""")

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
