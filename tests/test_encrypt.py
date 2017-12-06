#!/usr/bin/env python
"""
 Created by howie.hu at 06/12/2017.
"""

from toapi.encrypt import encrypt, decrypt


def test_encrypt():
    key = "L9qeRO25ojyXv37aWwrKpSAPYzVg6kBT"
    assert decrypt(encrypt('/toapi?hello=world', key), key) == "/toapi?hello=world"
