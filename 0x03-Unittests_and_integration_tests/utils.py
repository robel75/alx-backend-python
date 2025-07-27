#!/usr/bin/env python3
"""Utilities module"""

def memoize(method):
    """Memoization decorator"""
    attr_name = "_memoized_" + method.name

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

    return wrapper
