#!/usr/bin/env python3

# File: wip.py  (work in progress, for development)

"""
window types:
    collect a record/dict
        use code/textual/get_fields()
    choose from a listing of options/strings
                            functions
        use code/textual/menu()

# Code being developed here eventually to be
# moved into code/textual.py
"""

import PySimpleGUI as sg
from code import helpers
from code import routines
from code import textual

def params(one, two, kw1="kw1", kw2='kw2'):
    print(f"one: {one}")
    print(f"two: {two}")
    print(f"kw1: {kw1}")
    print(f"kw2: {kw2}")

def test_params():
    params(two=2, one=1, kw1="KW1", kw2="KW2")

if __name__ == "__main__":
    pass
#   test_params()
#   _ = input("W)ork i)n P)rogress...  Any key to continue")

