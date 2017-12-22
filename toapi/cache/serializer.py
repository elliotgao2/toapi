#!/usr/bin/env python

from toapi.cache.base_cache import BaseSerializer

try:
    import ujson as json
except ImportError:
    import json

try:
    import cPickle as pickle
except ImportError:
    import pickle


class JsonSerializer(BaseSerializer):
    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: dict
        :return: string
        """
        return json.dumps(value) if value is not None else ''

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: string
        :return: dict
        """
        return json.loads(value) if value is not None else {}


class PickleSerializer(BaseSerializer):
    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: object
        :return: bytes
        """
        return pickle.dumps(value)

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: bytes
        :return: object
        """
        return pickle.loads(value) if value is not None else value
