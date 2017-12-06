from toapi.selector import Selector


def with_metaclass(meta):
    return meta("toapi", (object,), {})


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


class Item(with_metaclass(ItemType)):
    """Parse item from html"""

    @classmethod
    def parse(cls, html):
        """Parse html to json"""
        if cls.Meta.source is None:
            return cls._parse_item(html)
        else:
            sections = cls.Meta.source.parse(html)
            results = []
            for section in sections:
                results.append(cls._parse_item(section))
            return results

    @classmethod
    def _parse_item(cls, html):
        item = {}
        cls._clean_item(html=html)
        for name in cls.selectors:
            try:
                item[name] = getattr(cls, name)
            except IndexError:
                item[name] = ''
            except Exception:
                item[name] = ''
        return item

    @classmethod
    def _clean_item(cls, html):
        for field_name, field_value in cls.selectors.items():
            get_field = getattr(cls, 'clean_%s' % field_name, None)
            value = field_value.parse(html) if isinstance(field_value, Selector) else field_value
            if get_field:
                value = get_field(cls(), value)
            setattr(cls, field_name, value)

    class Meta:
        source = None
        route = '\.+'
