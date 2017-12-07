#!/usr/bin/env python

import random
import string

from toapi.encrypt import encrypt, decrypt


def test_encrypt():
    key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    assert decrypt(encrypt('/toapi?hello=world', key), key) == "/toapi?hello=world"
