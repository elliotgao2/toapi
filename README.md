# toapi

[![CI](https://github.com/elliotgao2/toapi/actions/workflows/ci.yml/badge.svg)](https://github.com/elliotgao2/toapi/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/toapi.svg)](https://pypi.org/project/toapi/)
[![Python](https://img.shields.io/pypi/pyversions/toapi.svg)](https://pypi.org/project/toapi/)
[![License](https://img.shields.io/pypi/l/toapi.svg)](https://pypi.org/project/toapi/)

> Turn any website into a JSON API — declaratively.

`toapi` lets you point at a web page, declare the fields you want with CSS
selectors, and get back a clean JSON API. No crawler to babysit, no database to
maintain — pages are fetched and parsed on demand, with built‑in caching.

## Install

```bash
pip install toapi
```

Requires Python 3.10+.

## Quickstart

```python
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


api.run(host="127.0.0.1", port=5000)
```

Run it:

```bash
python app.py
```

Then visit <http://127.0.0.1:5000/posts> and you get:

```json
{
  "Post": [
    {"title": "Mathematicians Crack the Cursed Curve", "url": "https://www.quantamagazine.org/..."},
    {"title": "Stuffing a Tesla Drivetrain into a 1981 Honda Accord", "url": "https://jalopnik.com/..."}
  ]
}
```

## How it works

```
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │  /posts    │ ─▶ │  fetch     │ ─▶ │  parse     │ ─▶  JSON
   │  (route)   │    │  (cache)   │    │  (Item)    │
   └────────────┘    └────────────┘    └────────────┘
```

1. **Route** — `@api.route("/posts", "/news")` maps your API path to a source URL.
2. **Fetch** — pages are fetched with `requests` (or a headless browser if you pass `browser=`) and cached in memory.
3. **Parse** — each `Item` extracts fields with CSS selectors via `htmlparsing`.
4. **Serve** — Flask returns the result as JSON; subsequent calls hit the cache.

## Features

- **Declarative** — describe data, not scraping logic.
- **Routes** — map clean API paths to messy source URLs with `{param}` placeholders.
- **Multi-site** — merge several websites behind one API.
- **Cleaning hooks** — define `clean_<field>` methods to post-process values.
- **Caching** — pages and parsed results are cached automatically.
- **Headless browser** — pass `Api(browser="/path/to/geckodriver")` for JS-heavy sites.

## Cleaning values

Add a `clean_<fieldname>` method on the Item to transform a value before it's
returned:

```python
@api.site("https://news.ycombinator.com")
@api.route("/posts", "/news")
class Page(Item):
    next_page = Attr(".morelink", "href")

    def clean_next_page(self, value):
        return f"/posts?{value.split('?', 1)[1]}"
```

## Development

```bash
git clone https://github.com/elliotgao2/toapi.git
cd toapi
uv sync          # install deps into .venv
uv run pytest    # run tests
uv run ruff check .
```

We use [uv](https://github.com/astral-sh/uv) for packaging and
[ruff](https://github.com/astral-sh/ruff) for lint + format. Pre-commit hooks
keep both clean:

```bash
uv run pre-commit install
```

## Contributing

Pull requests are welcome. For non-trivial changes, please open an issue first
to discuss what you'd like to change. Make sure `uv run pytest` and
`uv run ruff check .` pass before submitting.

## License

[MIT](LICENSE) © Elliot Gao
