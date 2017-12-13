#!/usr/bin/env python

from toapi import Item, Regex


class User(Item):
    use_id = Regex(rule='"profilePage_(.*?)"')
    user_info_url = Regex(rule='"profilePage_(.*?)"')
    photos = Regex(rule='<a href="(/p/.*?)/"')

    def clean_photos(self, photos):
        return ["http://0.0.0.0:5000" + url for url in photos]

    def clean_use_id(self, user_info_url):
        return ''.join(user_info_url) if isinstance(user_info_url, list) else user_info_url

    def clean_user_info_url(self, user_info_url):
        return "https://i.instagram.com/api/v1/users/{}/info/".format(user_info_url[0])

    class Meta:
        source = None
        route = '/(?!p/)'

        web = {
            "with_ajax": True
        }
