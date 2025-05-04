#!/usr/bin/env python3

# File: utils/scan.py

"""
This code is being written with the goal of collecting the names of
all methods in each module and then checking each module where the
method in question is _not_ defined for the existence of a call or
reference to that module and providing a listing of the line numbers
for each.

Data Structuring:
master[filename][func_name][filename][list_of_locations]
  master:
    dict keyed by 'code_file_names'
      values are dicts keyed by the names of functions defined there.
        values are dicts keyed by 'codefile_name" (all but the file in
        which the function was defined) (We don't locate functions used
        in the file in which they are declared. (subject to chane))
            values are listings of the locations where the function
            is called or referenced in the file.

Tests found in tests/test_utils_scan.py.
"""

import sys
import re

code_files = """ alchemy.py ap_update.py attrition.py backupdata.py
ck_data.py club.py commands.py content.py data_entry.py dates.py
dock_change.py emailing.py fees.py gates.py get_data_byID.py
helpers.py leadership.py listings.py members.py mta.py multiple.py
old_member.py review.py routines.py show.py textual.py """.split()


def find_words_in_line(word, line):
    """
    Returns a (possibly empty) list of indices where word is found.
    Tested
    """
    res = []
    begin = 0
    l = len(line)
    while True:
        n = line.find(word, begin)
        if n == -1:
            break
        begin = n + len(word) #set up for next round
        # begin is now index immediately following our word
        # check that 'word' is not part of another word:
        if (((n >0) and (line[n-1].isalnum() or line[n-1]=="_"))
            # word doesn't begin here!
        or (begin==l or line[begin].isalnum() or line[begin]=='_')):
            #only the 1st part of another word!
            continue
        res.append(n)
    return res

def re2find_words(word, line):
    pass

# regular expressions are compiled into pattern objects (_po)
#word_po = re.compile(r"")
func_po = re.compile(r"def [a-zA-Z]+[a-zA-Z0-1_]*\(")
def find_func_def(line):
    """ Returns None or a match object. Tested """
    return func_po(line)

def find_func_call(func_name, line):
    """
    returns a listing of line locations where func_name is called
    or None if not found.
    """
    pass

def find(item, text):
    """
    Splits (on "\n") text into a sequence of <lines>.
    Returns a list of tuples: line and column
    where text represented by <item> is found.
    So far only testing framework has been created
    """
    lines = text.split("\n")
    locations = []
    lineN = 0
    for line in lines:
        lineN += 1
        begin = 0
        while True:
            location = line.find(item+"(", begin)
            if location == -1: break
            begin = location + len(item)
            if (location>0) and line[location-1].isalnum():
                continue
            locations.append((lineN, location))
    return locations

def find_func_def(line):
    """
    Looks for a function definition within <line>.
    Returns the function's name (if found) or None 
    Tested
    """
    fname = None
    _def = "def "
    b = line.find(_def)
    if b > -1:
        b += len(_def)
        e = line.find('(',b)
        fname = line[b:e]
    return fname

def module_name(stream_name):
    """
    Accepts "stream.name" from 'open(fname) as stream
    and returns 'fname'.  Tested
    """
    n = stream_name.find('/')
    e = stream_name.find('.')
    return stream_name[n+1:e]

def collect_data():
    """
    Not tested
    """
    master = dict()
    for f in code_files:
        with open("code/" + f, 'r') as stream:
            key = f"{stream.name}"
            module = module_name(key)
            master[key] = dict()
            for line in stream:
                found_def = find_func_def(line)
                if found_def:
                    master[key][found_def] = dict()

#   for key, value in master.items():
#       _ = input(f"{key}: {value}")
    above_yields = """
code/alchemy.py: {'alch': {}, 'task1': {}, 'task2': {}, 'get_dues': {}, 'show_dues_owing': {}, 'get_dock_fees_owed': {}, 'show_dock_fees_owed': {}, 'get_kayak_fees_owed': {}, 'show_kayak_fees_owed': {}, 'get_mooring_fees_owed': {}, 'show_mooring_fees_owed': {}}
"""

    for f in code_files:
        with open("code/" + f, 'r') as stream:
            text = stream.read()
            f_name = stream.name  # file name
            m_name = f_name.split('.')[0].split('/')[1]  # module name
        # collect function calls in files other than where defined
#       _ = input(repr(sorted(list(set(master.keys())-{f_name}))))
        for key in sorted(set(master.keys())-{f_name}):
            for func_name in master[key].keys():
                target = f"{m_name}.{func_name}"
                finding = find(target, text)
                if finding:
                    master[key][func_name][f_name] = finding
    return master


def show(data):
    """
    Not tested - only framework provided
    """
    for key, value in data.items():
        print(f"{key}:")  #source file
        for k, v in value.items():  # func_name, file_name
            print(f"\t{k}: ")  # func name
            for kk, vv in v.items():
                print(f"\t\t{kk}: ",end='')
                print(f"{vv}")

def exercise_find():
    """ Exercise 'find(item, lines)' """
    fname = "code/data_entry.py"
    target = "add2report"
    outf = "output.txt"
    with open(fname, 'r') as stream:
        text = stream.read()
    locations = find(target, text)
    with open(outf, "w") as stream:
        stream.write(", ".join([repr(location) for location in
                                locations]))
    print(f"Found '{target}' {len(locations)} times within {fname}")
    print(f"Results sent to {outf}.")
    output = """
    'lib.func(', 'mylib.func(': returned: '[]', expected: '[]'
    'lib.func(', 'lib.func(': returned: '[0]', expected: '[0]'
    'lib.func(', ' lib.func( ': returned: '[1]', expected: '[1]'
    'lib.func(', '(lib.func(param) ': returned: '[1]', expected: '[1]'
    'lib.func(', ' lib.func(param1)  lib.func(param2)': returned: '[1, 19]', expected: '[1, 19]'
    'lib.func(', 'just random text': returned: '[]', expected: '[]'
    'lib.func(', '   ': returned: '[]', expected: '[]'
    """

def ck_findwordinline():
    """
        [] 0
        [0] 0
        [1] 1
        [1] 1
        [1, 19] (1, 19)
        [] ()
        [] ()
    """
    findwordinline_data = [
            ("mylib.func(", []),
            ("lib.func(", [0]),
            (" lib.func( ", [1]),
            ("(lib.func(param) ", [1]),
            (" lib.func(param1)  lib.func(param2)", [1, 19]),
            ("just random text", []),
            ("   ", []),
            ]
    target = "lib.func("
    for line, res in findwordinline_data:
        ret = find_words_in_line(target, line)
        print(
            f"'{target}', '{line}': returned: '{ret}', expected: '{res}'")

if __name__ == "__main__":
    res =find_words_in_line("lib.func(", " lib.func( ")
    print(f"{res} should be [1]")
#   print(find_func_def("   def func_declaration(params):  "))
#   ck_findwordinline()
#   collect_data()
#   show(collect_data())
#   exercise_find()
