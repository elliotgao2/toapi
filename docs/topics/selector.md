# Selectors

`toapi` doesn't ship its own selectors — it uses the ones from
[`htmlparsing`](https://pypi.org/project/htmlparsing/). Import them directly:

```python
from htmlparsing import Attr, Text
```

## `Text(css)`

Extracts the text content of the first element matching `css`.

```python
title = Text(".titleline > a")
```

## `Attr(css, name)`

Extracts the value of the `name` attribute on the first element matching
`css`.

```python
url = Attr(".titleline > a", "href")
image = Attr("img.thumbnail", "src")
```

## Choosing selectors

Selectors are plain CSS, so anything that works in your browser's DevTools
works here. A few tips:

- **Inspect first.** Open the source page in DevTools and right-click → *Copy
  selector* to get a starting point.
- **Be specific.** Class names like `.title` are often reused; combine with
  parent selectors (`.story .title`) for stability.
- **Watch for SSR vs JS.** If the data only appears after JavaScript runs,
  CSS selectors won't see it — pass `browser="/path/to/geckodriver"` to `Api`
  to render with a real browser.

## Cleaning vs selecting

Selectors only *find* values. To transform them (URL rewriting, type casting,
normalizing whitespace), use a `clean_<field>` method on the Item — see
[Item](item.md).
