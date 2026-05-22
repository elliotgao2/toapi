from htmlparsing import HTMLParsing, Selector


class Item:
    _list: bool | None = None
    _site: str | None = None
    _selector: str | None = None
    __fields__: dict[str, Selector] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        fields: dict[str, Selector] = {}
        for name, value in list(vars(cls).items()):
            if isinstance(value, Selector):
                fields[name] = value
                delattr(cls, name)
        cls.__fields__ = fields
        cls._list = None
        cls._site = None
        cls._selector = None

    @classmethod
    def parse(cls, html: str):
        if cls._list:
            result = HTMLParsing(html).list(cls._selector, cls.__fields__)
            return [cls._clean(item) for item in result]
        result = HTMLParsing(html).detail(cls.__fields__)
        return cls._clean(result)

    @classmethod
    def _clean(cls, item: dict) -> dict:
        for name in cls.__fields__:
            clean = getattr(cls, f"clean_{name}", None)
            if clean is not None:
                item[name] = clean(cls, item[name])
        return item
