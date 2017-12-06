#!/usr/bin/env python
import functools


def dec_connector(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._cache_conn is None:
            self._cache_conn = self._connector()
            return func(self, *args, **kwargs)

        return func(self, *args, **kwargs)

    return wrapper
