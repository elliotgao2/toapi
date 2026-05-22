from unittest.mock import patch

import pytest
from htmlparsing import Attr, Text
from webtest import TestApp as App

from toapi import Api, Item
from toapi.cli import cli

SAMPLE_HTML = """
<html><body>
  <table>
    <tr class="athing">
      <td><span class="titleline"><a href="https://example.com/1">First story</a></span></td>
    </tr>
    <tr class="athing">
      <td><span class="titleline"><a href="https://example.com/2">Second story</a></span></td>
    </tr>
  </table>
  <a class="morelink" href="news?p=2">More</a>
</body></html>
"""


class FakeResponse:
    content = SAMPLE_HTML.encode("utf-8")


@pytest.fixture
def fake_get():
    with patch("toapi.api.requests.get", return_value=FakeResponse()) as mock:
        yield mock


def test_list_item_parses_each_row(fake_get):
    api = Api()

    @api.site("https://example.com")
    @api.list(".athing")
    @api.route("/posts", "/news")
    class Post(Item):
        title = Text(".titleline > a")
        url = Attr(".titleline > a", "href")

    app = App(api.app)
    body = app.get("/posts").json
    assert body["Post"] == [
        {"title": "First story", "url": "https://example.com/1"},
        {"title": "Second story", "url": "https://example.com/2"},
    ]


def test_detail_item_returns_single_dict(fake_get):
    api = Api()

    @api.site("https://example.com")
    @api.route("/page", "/news")
    class Page(Item):
        next_page = Attr(".morelink", "href")

    app = App(api.app)
    body = app.get("/page").json
    assert body["Page"] == {"next_page": "news?p=2"}


def test_clean_method_transforms_field(fake_get):
    api = Api()

    @api.site("https://example.com")
    @api.route("/page", "/news")
    class Page(Item):
        next_page = Attr(".morelink", "href")

        def clean_next_page(self, value):
            return f"/wrapped/{value}"

    app = App(api.app)
    body = app.get("/page").json
    assert body["Page"]["next_page"] == "/wrapped/news?p=2"


def test_multiple_items_merge_into_one_response(fake_get):
    api = Api()

    @api.site("https://example.com")
    @api.list(".athing")
    @api.route("/feed", "/news")
    class Post(Item):
        title = Text(".titleline > a")

    @api.site("https://example.com")
    @api.route("/feed", "/news")
    class Pager(Item):
        next_page = Attr(".morelink", "href")

    app = App(api.app)
    body = app.get("/feed").json
    assert len(body["Post"]) == 2
    assert body["Pager"] == {"next_page": "news?p=2"}


def test_handler_returns_500_when_parsing_fails(fake_get):
    api = Api()

    @api.site("https://example.com")
    @api.list(".athing")
    @api.route("/posts", "/news")
    class Post(Item):
        missing = Attr(".does-not-exist", "href")

    app = App(api.app)
    with pytest.raises(Exception):
        app.get("/posts")


def test_cli_is_importable_and_callable():
    assert callable(cli)


def test_run_exits_on_invalid_port():
    api = Api()
    with pytest.raises(SystemExit):
        api.run(port=-1)
