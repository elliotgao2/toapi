#!/usr/bin/env python
from toapi import Api

from items.image_info import ImageInfo
from items.use import User
from settings import MySettings

api = Api('https://www.instagram.com', settings=MySettings)

api.register(ImageInfo)
api.register(User)


api.serve(ip='0.0.0.0', port='5000')
