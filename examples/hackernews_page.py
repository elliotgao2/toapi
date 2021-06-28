from flask import request
from htmlparsing import Attr, Text

from toapi import Api, Item

api = Api(browser="/home/bug/桌面/geckodriver")


@api.site("https://news.ycombinator.com")
@api.list(".athing")
@api.route("/posts?page={page}", "/news?p={page}")
@api.route("/posts", "/news?p=1")
class Post(Item):
    url = Attr(".storylink", "href")
    title = Text(".storylink")


@api.site("https://news.ycombinator.com")
@api.route("/posts?page={page}", "/news?p={page}")
@api.route("/posts", "/news?p=1")
class Page(Item):
    next_page = Attr(".morelink", "href")

    def clean_next_page(self, value):
        return api.convert_string(
            "/" + value,
            "/news?p={page}",
            request.host_url.strip("/") + "/posts?page={page}",
        )


api.run(debug=True, host="0.0.0.0", port=5000)
