#!/usr/bin/env python3

# File: erd.py  (Entity Relationship Diagram)

"""
    Written to allow schema to be displayed on one page [1]
    to serve as an "Entity Relationship Diagram."
    Specifically, create a single file with two columns
    from a schema defining source file.
    There must be a form feed ('i\V\F' if using vim) 
    in the input file to mark the end of the first column
    and the beginning of the second.

    Usage:
        ./erd.py [inf [outf]]

    <infile> +/- <outfile> may be specified.
    If not specified, defaults are provided.

    A header has also been added.

    [1] The 'create_tables.sql' file is a bit less than
    two pages long; this utility puts all the content 
    onto one page in two columns.
    It's expected that most sqlite3 db creating command
    sequences will probably be of similar length.
"""

import sys

source = 'Sql/create_tables.sql'
destination = 'ERD.txt'
preface_lines = ['',
        '-- Data Base Schema',
        '-- AKA Entity Relationship Diagram (ERD)',
        ]


def split_file(source):
    """
    """
    with open(source, 'r') as instream:
        donewithleadingcomments = False
        collector1 = []
        collector2 = []
        collector = collector1
        for line in instream:
            if not line.startswith('--'):
                donewithleadingcomments = True
            if donewithleadingcomments:
                if line.startswith(''):
                    collector = collector2
                    collector.append('\n')
                else:
                    collector.append(line.rstrip())
    l1 = len(collector1)
    l2 = len(collector2)
    if l1 > l2:
        while len(collector2) < l1:
            collector2.append('')
    elif l2 > l1:
        while len(collector1) < l2:
            collector2.append('')
    return((collector1, collector2))


def combine(part1, part2):
    line_f = "{:<40} {}"
    res = []
    parts = zip(part1, part2)
    for part1, part2 in parts:
        res.append(line_f.format(part1, part2))
    return res 


if __name__ == '__main__':
    # set up file names:
    if len(sys.argv) >= 2:
        infile = sys.argv[1]
    else:
        infile = source
    if len(sys.argv) >= 3:
        outf = sys.argv[2]
    else:
        outf = destination
    # get the data:
    col1, col2 = split_file(infile)
    text = '\n'.join(combine(col1, col2))

    # yield the result:
    if outf:
        with open(outf, 'w') as outstream:
            for line in preface_lines:
                outstream.write(line+'\n')
            outstream.write(text)
    else:
        for line in preface_lines:
            print(line)
        print(text)

