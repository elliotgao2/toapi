from collections import OrderedDict


class ItemType(type):
    def __new__(cls, what, bases=None, attrdict=None):
        __fields__ = OrderedDict()

        for name, selector in attrdict.items():
            if name not in ('__module__', '__qualname__'):
                __fields__[name] = selector

        attrdict['__fields__'] = __fields__

        for name in __fields__.keys():
            del attrdict[name]
        instance = type.__new__(cls, what, bases, attrdict)
        instance._list = None
        instance._base_url = None
        instance._selector = None
        return instance

    def __repr__(self):
        return 'Item<{}>'.format(self.__name__)


class Item(metaclass=ItemType):
    """"""
