from toapi.selector import Selector, XPath


class ItemType(type):
    def __new__(cls, what, bases=None, dict=None):
        selectors = {}
        for name, selector in dict.items():
            if isinstance(selector, Selector):
                selectors[name] = selector
        dict['selectors'] = selectors
        dict['name'] = what.lower()
        for name in selectors:
            del dict[name]
        return type.__new__(cls, what, bases, dict)


class Item(metaclass=ItemType):
    """Parse item from html"""

    @classmethod
    def parse(cls, html):
        """Parse html to json"""
        sections = cls.Meta.source.parse(html)
        results = []
        for section in sections:
            item = {}
            for name in cls.selectors:
                item[name] = cls.selectors[name].parse(section)
            results.append(item)
        return results

    class Meta:
        source = XPath('//*')
        route = '\.+'
