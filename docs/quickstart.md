# Quickstart

Build a small API in front of Hacker News. By the end you'll have two routes,
a list of posts, and a cleaned `next_page` URL that loops back into your own
API.

## 1. Install

```bash
pip install toapi
```

Requires Python 3.10+.

## 2. Write `app.py`

```python
from flask import request
from htmlparsing import Attr, Text
from toapi import Api, Item

api = Api()


@api.site("https://news.ycombinator.com")
@api.list(".athing")
@api.route("/posts", "/news")
@api.route("/posts?page={page}", "/news?p={page}")
class Post(Item):
    title = Text(".titleline > a")
    url = Attr(".titleline > a", "href")


@api.site("https://news.ycombinator.com")
@api.route("/posts", "/news")
@api.route("/posts?page={page}", "/news?p={page}")
class Page(Item):
    next_page = Attr(".morelink", "href")

    def clean_next_page(self, value):
        return api.convert_string(
            "/" + value,
            "/news?p={page}",
            request.host_url.strip("/") + "/posts?page={page}",
        )


api.run(host="127.0.0.1", port=5000)
```

## 3. Run

```bash
python app.py
```

Then open <http://127.0.0.1:5000/posts>:

```json
{
  "Post": [
    {"title": "Mathematicians Crack the Cursed Curve", "url": "https://..."},
    {"title": "Stuffing a Tesla Drivetrain into a 1981 Honda Accord", "url": "https://..."}
  ],
  "Page": {
    "next_page": "http://127.0.0.1:5000/posts?page=2"
  }
}
```

## What just happened?

- `@api.site(...)` told the item which website to scrape from.
- `@api.list(".athing")` said *this item repeats* — each `.athing` element on
  the page becomes one entry.
- `@api.route(api_path, source_path)` mapped the path your users hit to the
  path on the source site. `{page}` is a placeholder passed through both
  directions.
- `Text(...)` and `Attr(...)` are CSS selectors that pull a value out of each
  matched element.
- `clean_next_page(self, value)` runs after parsing and rewrites the source
  pagination link to point back at our own API.

That's the whole framework. See [Topics](topics/api.md) for the details.
