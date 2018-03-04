from collections import OrderedDict

from htmlparsing import Selector, HTMLParsing


class ItemType(type):
    def __new__(cls, what, bases=None, attrdict=None):
        __fields__ = OrderedDict()

        for name, selector in attrdict.items():
            if isinstance(selector, Selector):
                __fields__[name] = selector

        for name in __fields__.keys():
            del attrdict[name]

        instance = type.__new__(cls, what, bases, attrdict)
        instance._list = None
        instance._site = None
        instance._selector = None
        instance.__fields__ = __fields__
        return instance


class Item(metaclass=ItemType):

    @classmethod
    def parse(cls, html: str):
        if cls._list:
            result = HTMLParsing(html).list(cls._selector, cls.__fields__)
            result = [cls._clean(item) for item in result]
        else:
            result = HTMLParsing(html).detail(cls.__fields__)
            result = cls._clean(result)
        return result

    @classmethod
    def _clean(cls, item):
        for name, selector in cls.__fields__.items():
            clean_method = getattr(cls, 'clean_%s' % name, None)
            if clean_method is not None:
                item[name] = clean_method(cls, item[name])
        return item
