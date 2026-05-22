# Api

`Api` is the entry point. It owns the Flask app, the cache, and the registry
of routes.

```python
from toapi import Api

api = Api()
```

## Constructor

```python
Api(site: str = "", browser: str | None = None)
```

- **`site`** — a default base URL prefix appended in front of every Item's
  source path. Most users leave this blank and put the site on the Item with
  `@api.site(...)`.
- **`browser`** — path to a headless-browser driver (e.g. `geckodriver`).
  When set, pages are fetched through the browser instead of plain
  `requests`. Useful for JavaScript-heavy sites.

## Decorators

Decorators are stacked on an `Item` class to declare *what* to scrape,
*where* it lives, and *which URLs* expose it.

### `@api.site(url)`

Sets the source website for an Item.

```python
@api.site("https://news.ycombinator.com")
class Post(Item): ...
```

### `@api.list(selector)`

Marks the Item as a *list item* — the parser will return one entry per
element matched by `selector` on the source page.

```python
@api.list(".athing")
class Post(Item): ...
```

Without `@api.list`, the Item is a *detail item* — it parses a single record
from the page.

### `@api.route(api_path, source_path)`

Maps a path on your API to a path on the source site. Placeholders like
`{page}` are passed through both directions.

```python
@api.route("/posts?page={page}", "/news?p={page}")
@api.route("/posts", "/news")
class Post(Item): ...
```

Multiple `@api.route` decorators may be stacked on the same Item.

## `api.run(host, port, **flask_options)`

Starts the Flask development server.

```python
api.run(host="0.0.0.0", port=5000, debug=True)
```

For production, mount `api.app` (a plain Flask app) under your WSGI server of
choice — gunicorn, uWSGI, waitress.

## Caching

Two in-memory caches are populated automatically:

- **Page cache** (`api._storage`) — keyed by source URL, stores raw HTML.
- **Result cache** (`api._cache`) — keyed by API path, stores parsed JSON.

Both live for the lifetime of the process. Restart to clear.
