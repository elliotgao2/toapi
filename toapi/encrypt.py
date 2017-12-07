#!/usr/bin/env python
import base64
import random
import string

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def encrypt(text, key):
    """
    Encrypt the string
    :param text: eg: /toapi?hello=world
    :param key:
    :return: str
    """
    if len(text) % 16 != 0:
        text = text + str((16 - len(text) % 16) * '&')
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    cipher_text = cipher.encrypt(text)
    return str(base64.b64encode(b2a_hex(cipher_text)), encoding='utf-8')


def decrypt(text, key):
    """
    Decrypt the string or bytes
    """
    if isinstance(text, str):
        text = bytes(text, encoding="utf8")
    cipher_text = base64.b64decode(text)
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    plain_text = cipher.decrypt(a2b_hex(cipher_text))
    return str(plain_text, encoding='utf-8').rstrip('&')


def gen_key():
    """
    Generate a key
    :return: str
    """
    key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return key
