#!/usr/bin/env python
from toapi.settings import Settings


class MySettings(Settings):
    """
    Create custom configuration
    """
    with_ajax = True
