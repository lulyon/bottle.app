# -*- coding: utf-8 -*-

""" two methods that helps dealing with unicode """

def decode(value):
    """ decode(ascii) -> unicode """
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    return value

def encode(value):
    """ encode(unicode) -> ascii """
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    return value