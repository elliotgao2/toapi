#!/usr/bin/env python
import functools


def dec_connector(func):
    @functools.wraps(func)
    def wrapper(self, *args, connector=None, **kwargs):
        if connector is None:
            connector = self._connector()
            return func(self, *args, connector=connector, **kwargs)

        return func(self, *args, connector=connector, **kwargs)

    return wrapper
