#!/usr/bin/env python3

# File: find.py

"""
"""

def test_find():
    mylib.func(                            []
lib.func(                              [0]
 lib.func(                             [1]
(lib.func(param)                       [1]
 lib.func(param1)  lib.func(param2)    [1, 19]
just random text                       []
                                       []

    test_data = [
            ("mylib.func(", (0)),
            ("lib.func(", (0)),
            (" lib.func( ", (1)),
            ("(lib.func(param) ", (1)),
            (" lib.func(param1)  lib.func(param2)", (1, 19)),
            ("just random text", ()),
            ("   ", ()),
            ]

    for line in [
            "mylib.func(",
            "lib.func(",
            " lib.func( ",
            "(lib.func(param) ",
            " lib.func(param1)  lib.func(param2)",
            "just random text",
            "   ",
            ]:
        res = find_word_in_line("lib.func(", line)
        print(f"{line:<37}  {res}")

if __name__ == "__main__":
    test_find()
