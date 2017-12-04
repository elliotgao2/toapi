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
                try:
                    item[name] = cls.selectors[name].parse(section)[0]
                except IndexError:
                    item[name] = ''
            results.append(item)
        return results

    class Meta:
        source = XPath('//*')
        route = '\.+'
