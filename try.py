#!/usr/bin/env python3

"""
A place to prototype new code.
"""

from code import helpers
#from code import routines
#from code import dates

class RecV1(dict):
    """
    Each instance is a (deep!) copy of rec (a dict)
    and is callable (with a formatting string as a parameter)
    returning the populated formatting string.

    """
    def __init__(self, rec):
#       self = dict(rec)  # this should work but doesn't!!
        for key, value in rec.items():   #} use this method in 
            self[key] = value            #} place of what's above

    def __call__(self, fstr):
        return fstr.format(**self)

def func1():
    l = ["hello", "bye", "so long", ]
    s = set(l)
    print(f"{s}")

def func2():
    d1 = {"husband": "Alex", "wife": "June",
            "daughter": "Tanya", "son": "Kelly", }
#   d2 = dict(d1)
    d2 = helpers.Rec(d1)
    d2["grand_daughter"] = "Isabella"
    print(d1)
    print(d2)
    print(f"it's {d1 is d2} that d1 is d2.")
    print(d2("Wife's name is {wife}."))


if __name__ == "__main__":
    func2()

