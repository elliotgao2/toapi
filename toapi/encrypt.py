#!/usr/bin/env python
import base64

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def encrypt(text, key):
    if len(text) % 16 != 0:
        text = text + str((16 - len(text) % 16) * '&')
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    cipher_text = cipher.encrypt(text)
    return base64.b64encode(b2a_hex(cipher_text))


def decrypt(text, key):
    if isinstance(text, str):
        text = bytes(text, encoding="utf8")
    cipher_text = base64.b64decode(text)
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    plain_text = cipher.decrypt(a2b_hex(cipher_text))
    return str(plain_text, encoding='utf-8').rstrip('&')
