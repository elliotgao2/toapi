#!/usr/bin/env python
from toapi.settings import Settings


class MySettings(Settings):
    """
    Create custom configuration
    """
    web_config = {
        "with_ajax": False,
        "request_config": {
            'proxies': {
                'http': '0.0.0.0:8118',
                'https': '0.0.0.0:8118'
            }
        },
        "headers": None
    }
