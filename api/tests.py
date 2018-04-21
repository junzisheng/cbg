from django.test import TestCase

# Create your tests here.

__all__ = ["cal1"]

_g = None

class _Calculate(object):
    def __init__(self): pass

    def cal1(self):
        # do some calculate
        return

if _g is None:
    _g = _Calculate()

def cal1():
    return _g.cal1()

cal1()
