from toapi.settings import Settings


class MySettings(Settings):
    cache = {
        'type': 'redis',
        'url': '127.0.0.0.1:6789/0'
    }
    storage = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
