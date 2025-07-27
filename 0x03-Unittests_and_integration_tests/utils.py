#!/usr/bin/env python3
"""Utils module"""
import requests
from functools import wraps


def access_nested_map(nested_map, path):
    """Access nested map with a path"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """Get JSON from URL"""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Memoize decorator"""
    attr_name = "_{}".format(fn.name)

    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper
