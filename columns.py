#!/usr/bin/env python3

# File: columns.py

"""
    Written to allow schema to be displayed on one page.
    Specifically, create two files (ct1 and ct2) from the
    first and second half of the create_schema.sql file.
    Usage:
        ./columns.py [f1 f2 [of]]

    f1, f2 & of are file names (defaults: ct1, ct2, stdout.)
    The first two are assumed to contain short lines
    The output (sent to <of> if specified or stdout if not)
    will have content of f1 on the left side and of f2 on
    the right side of the output page.
    A header has also been added.
"""

import sys


def read_into(f):
    """
    Returns a sequence of lines read from <f> (a text file.)
    """
    ret = []
    with open(f, 'r') as stream:
        for line in stream:
            ret.append(line.rstrip())
    return ret


def combine(inf1, inf2):
    line_f = "{:<40} {}"
    res = []
    parts1 = read_into(inf1)
    parts2 = read_into(inf2)
    parts = zip(parts1, parts2)
    for part1, part2 in parts:
        res.append(line_f.format(part1, part2))
    return res 


if __name__ == '__main__':
    preface_lines = ['',
            '-- Data Base Schema',
            '-- AKA Entity Relationship Diagram (ERD)',
            '',
            '',
            ]
    # set up file names:
    if len(sys.argv) >= 3:
        ct1 = sys.argv[1]
        ct2 = sys.argv[2]
    else:
        ct1 = 'ct1'
        ct2 = 'ct2'
    if len(sys.argv) == 4:
        outf = sys.argv[3]
    else:
        outf = None

    # get the data:
    text = '\n'.join(combine(ct1, ct2))

    # yield the result:
    if outf:
        _ = input(outf)
        with open(outf, 'w') as outstream:
            for line in preface_lines:
                outstream.write(line+'\n')
            outstream.write(text)
    else:
        for line in preface_lines:
            print(line)
        print(text)

    
