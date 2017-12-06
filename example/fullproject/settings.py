from toapi.settings import Settings


class MySettings(Settings):
    cache = {
        'type': 'redis',
        'url': '127.0.0.0.1:6789/0'
    }
    storage = {
        'dir': './html/',
        'refresh': '10/min'
    }
    with_ajax = None
