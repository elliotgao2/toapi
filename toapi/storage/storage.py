from .db_store import DBStore
from .disk_store import DiskStore


class Storage:
    """
    transfer DBStore and DiskStore functions
    about param settings:
    settings = {
        "PATH": "/User/ToApi,
        "DB_URL": None
    }
    PATH: the path of local file stores, default path is current running file path
    DB_URL: store url source in db, ignoring local store if this param give
    """

    def __init__(self, settings):
        self.storage = getattr(settings, 'storage', {})
        self.path = self.storage.get("PATH")
        if not self.path:
            self.path = "./"
        self.db_url = self.storage.get("DB_URL")

        self.db_store = DBStore(self.db_url) if self.db_url else None
        self.disk_store = DiskStore(self.path) if not self.db_store else None

    def save(self, url, html):

        if not self.db_store:
            return self.disk_store.save(url, html)
        return self.db_store.save(url, html)

    def get(self, url, expiration="inf"):

        if not self.db_store:
            return self.disk_store.get(url=url, expiration=expiration)
        return self.db_store.get(url=url, expiration=expiration)
