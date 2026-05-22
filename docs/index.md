# toapi

> Turn any website into a JSON API — declaratively.

`toapi` lets you point at a web page, declare the fields you want with CSS
selectors, and get a clean JSON API back. No crawler to babysit, no database
to maintain — pages are fetched and parsed on demand, with built-in caching.

## A 10-line example

```python
from htmlparsing import Attr, Text
from toapi import Api, Item

api = Api()


@api.site("https://news.ycombinator.com")
@api.list(".athing")
@api.route("/posts", "/news")
class Post(Item):
    title = Text(".titleline > a")
    url = Attr(".titleline > a", "href")


api.run(host="127.0.0.1", port=5000)
```

Visit `http://127.0.0.1:5000/posts` and you get a JSON list of every story
on the front page.

## How it works

1. **Route** — `@api.route("/posts", "/news")` maps your API path to a source
   URL.
2. **Fetch** — pages are fetched with `requests` (or a headless browser if
   you pass `browser=`) and cached in memory.
3. **Parse** — each `Item` extracts fields with CSS selectors via
   `htmlparsing`.
4. **Serve** — Flask returns the result as JSON; subsequent calls hit the
   cache.

## Next steps

- [Quickstart](quickstart.md) — a complete walk-through with two routes and a
  clean method.
- [Api](topics/api.md) — the `Api` class and its decorators.
- [Item](topics/item.md) — how to declare data shapes.
- [Selectors](topics/selector.md) — picking values out of HTML.
