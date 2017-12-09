#!/usr/bin/env python
from toapi import Item, Css


class ImageInfo(Item):
    image_url = Css('head > meta[property="og:image"]', attr='content')
    description = Css('head > meta[property="og:description"]', attr='content')
    source_url = Css('head > meta[property="og:url"]', attr='content')
    user_id = Css('head > meta[property="instapp:owner_user_id"]', attr='content')
    user_info_url = Css('head > meta[property="instapp:owner_user_id"]', attr='content')

    def clean_user_info_url(self, user_info_url):
        return "https://i.instagram.com/api/v1/users/{}/info/".format(user_info_url[0])

    class Meta:
        source = None
        route = '/p/.*?'
