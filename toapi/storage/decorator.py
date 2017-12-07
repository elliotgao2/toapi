from .storage import DiskStore, DBStore
from functools import wraps


def disk_save(func):

    @wraps(func)
    def wrappers(*args, **kwargs):
        pass

    return wrappers


def db_save(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        pass

    return wrappers
