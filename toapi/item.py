from toapi.selector import Selector


def with_metaclass(meta):
    return meta("toapi", (object,), {})


class ItemType(type):
    def __new__(cls, what, bases=None, dict=None):
        __selectors__ = {}
        for name, selector in dict.items():
            if isinstance(selector, Selector):
                __selectors__[name] = selector
        dict['__selectors__'] = __selectors__
        dict['__base_url__'] = dict.get('__base_url__', None)
        for name in __selectors__.keys():
            del dict[name]

        instance = type.__new__(cls, what, bases, dict)
        instance.__name__ = dict.get('__name__', instance.__name__)
        return instance


class Item(with_metaclass(ItemType)):
    """Parse item from html"""

    @classmethod
    def parse(cls, html):
        """Parse html to json"""
        if cls.Meta.source is None:
            return cls._parse_item(html)
        else:
            sections = cls.Meta.source.parse(html, is_source=True)
            results = []
            for section in sections:
                results.append(cls._parse_item(section))
            return results

    @classmethod
    def _parse_item(cls, html):
        item = {}
        for name, selector in cls.__selectors__.items():

            try:
                item[name] = selector.parse(html)
            except Exception:
                item[name] = ''

            clean_method = getattr(cls, 'clean_%s' % name, None)

            if clean_method is not None:
                item[name] = clean_method(cls, item[name])

        return item

    class Meta:
        source = None
        route = {}
