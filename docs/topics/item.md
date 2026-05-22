# Item

An `Item` is a data shape. You declare what fields you want and how to find
them in the HTML; `toapi` does the rest.

```python
from htmlparsing import Attr, Text
from toapi import Item

class Post(Item):
    title = Text(".titleline > a")
    url = Attr(".titleline > a", "href")
```

Each class attribute that is a *Selector* (`Text`, `Attr`, etc. from
`htmlparsing`) becomes a field. Everything else stays a regular class
attribute or method.

## List vs detail

By default an Item is a *detail* — it produces a single dict from the page.

```python
{"title": "...", "url": "..."}
```

Decorating it with `@api.list(".something")` makes it a *list* — it produces
one dict per element matched by the selector.

```python
[{"title": "...", "url": "..."}, {"title": "...", "url": "..."}]
```

## Cleaning fields

To transform a field's value before it's returned, define `clean_<fieldname>`
on the Item:

```python
class Page(Item):
    next_page = Attr(".morelink", "href")

    def clean_next_page(self, value):
        return f"/posts?{value.split('?', 1)[1]}"
```

Clean methods receive the parsed value and return the transformed one. They
run after parsing, before caching, on every entry of a list item.

## Multiple Items per page

Several Items can share the same route. Their results are merged into one
JSON response, keyed by class name:

```python
@api.route("/posts", "/news")
@api.list(".athing")
class Post(Item): ...


@api.route("/posts", "/news")
class Page(Item):
    next_page = Attr(".morelink", "href")
```

```json
{
  "Post": [...],
  "Page": {"next_page": "..."}
}
```
