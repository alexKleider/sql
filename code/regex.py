#!/usr/bin/env python3

# File: regex.py

# "po" :: pattern object

import re

# regular expressions are compiled into pattern objects (_po)
word_po = re.compile(r"\b_*[a-zA-Z]\w*\b")
#word_po = re.compile(r"[\s|^[a-zA-Z]\w*")
#word_po = re.compile(r"[a-zA-Z]\w*")
#word_po = re.compile(r"word")
#func_po = re.compile(r"def [a-zA-Z]+[a-zA-Z0-1_]*\(")

test_data = [
        ("word", ["word"], [0]),
        (" word ", ["word"], [1]),
        ("word; ", ["word"], [0]),
        (" Word_suffix  ", ["Word_suffix"], []),
        (" junk.target:", ["junk", "target"], []),
        ("def target(", ["def", "target"], []),
        (" H3 ", ["H3"], []),
        (" H_4", ["H_4"], []),
        (" this word may not be the last word on topic",
         ["this", "word", "may", "not", "be", "the", "last", "word",
         "on", "topic"], [6, 31]),
        (" this underscored _word_ may not be a word_",
         ["this", "underscored", "_word_", "may", "not", "be", "a",
         "word_"], []),
        ("  wordsalad  ", ["wordsalad"], []),
        ("def myfunc(param1, param2,param3):",
         ["def", "myfunc", "param1", "param2", "param3"], []),
        ]

def check_word_po():
    for a, b, c in test_data:
        if not word_po.findall(a) == b:
            print(f"Error: {a} ==> {word_po.findall(a)}")
            print(f"{b} != word_po.findal(a)")



def re2find_word(word, line):
    """
    Returns (a possibly empty) list of locations where <word> appears
    in <line>.
    """
    _word = r"\b" + word + r"\b"
    word_po = re.compile(_word)
    mos = word_po.finditer(line)
    return [mo.start() for mo in mos]

def test_re2find_word():
    print("Looking for 'word'...")
    for a, b, c in test_data:
        if not re2find_word("word", a) == c:
            print(f"re2find_word('word', {a}) ==> {res} != {c}")

if __name__ == "__main__":
    print("running <check_word_po()>...")
    check_word_po()
    print("====================")
    print("running <test_re2find_word()>...")
    test_re2find_word()
