#!/usr/bin/env python3

# File: tests/func_tests.py

"""
Begun as a place to describe work flow.
_May_ eventually develope functional tests.
The following may or may not be true:
Currently simply prints out the content of each file in the Sql
directory (except 'create_tables.sql' and 'redo_DKM_tables.sql'.)
"""

import os


def queryFileNames():
    ret = os.listdir("Sql")
    return [name for name in ret if not name in (
        'create_tables.sql', 'redo_DKM_tables.sql')]
    

def queryDict():
    ret = {}
    filenames = queryFileNames()
    for name in [name for name in filenames if
            name.endswith(".sql")]:
        with open(os.path.join('Sql', name), 'r') as infile:
            query = infile.read()
        ret[name] = query
    return ret


scenarios = """
new application arrives:
    Use "add2People" to enter demographics into People table
    and the returned newly assigned personID to make entries
    into the Applicants (sponsors and dates) and Stati tables.

application fee arrives for an 'a-' applicant:

post meeting attendance updates:

reassign dues and fees:

report:

display for web:

"""

def main():
    for content in queryDict().values():
        print(content)


if __name__ == '__main__':
    main()
