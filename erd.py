#!/usr/bin/env python3

# File: erd.py  (Entity Relationship Diagram)

"""
    Written to allow schema to be displayed on one page [1]
    to serve as an "Entity Relationship Diagram."
    Specifically, create a single file with two columns
    based on the current schema of our data file (derived
    from the routines.py module.)

    Usage:
        ./erd.py [outfile]  # default: ERD.txt

"""

import sys
import datetime

try: from code import routines
except ImportError: import routines


today = datetime.datetime.today()
date_template = "%b %d, %Y"
date = datetime.datetime.strptime(
        today.strftime(date_template),
        date_template
            ).strftime(date_template)


def split_on_FF(source):
    """
    Source is an array of lines assumed to have a line somewhere
    near its middle beginning with the form feed character ('^L').
    Returned is a tuple of two listings of the lines: those
    before the form feed and those that follow it. Both listings
    are of the same length (having been padded with empty lines
    as needed.
    """
    collector1 = []
    collector2 = []
    collector = collector1
    for line in source:
        if line.startswith(''):
            collector = collector2
        else:
            collector.append(line)
    
    l1 = len(collector1)
    l2 = len(collector2)
    if l1 > l2:
        while len(collector2) < l1:
            collector2.append('')
    elif l2 > l1:
        while len(collector1) < l2:
            collector1.append('')
    return((collector1, collector2))


def combine(part1, part2):
    line_f = "    {:<38} {}"
    res = []
    parts = zip(part1, part2)
    for part1, part2 in parts:
        res.append(line_f.format(part1, part2))
    return res 


def get_schema_with_FF():
    """
    Gets the schema from our data base and inserts a 
    FormFeed character close to the middle
    returning an array of lines.
    This code is plagerized from
    https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    """
    ret = []
    lineNumber = 0
    lineNumbers = [0, ]
    query = """
            select NAME from SQLITE_MASTER where TYPE='table'
            -- order by NAME
            ;
            """
    for (tableName, ) in routines.fetch(query, from_file=False):
        ret.append('')
        ret.append("{}:".format(tableName))
        lineNumber += 2
        for (
            columnID, columnName, columnType,
            columnNotNull, columnDefault, columnPK,
        ) in routines.fetch("pragma table_info('{}');"
                .format(tableName), from_file=False):
            ret.append("  {id}: {name}({type}){null}{default}{pk}".format(
                id=columnID,
                name=columnName,
                type=columnType,
                null=" not null" if columnNotNull else "",
                default=" [{}]".format(columnDefault) if columnDefault else "",
                pk=" *{}".format(columnPK) if columnPK else "",
            ))
            lineNumber += 1
        lineNumbers.append(lineNumber)
    middleNumber = lineNumbers[-1]/2
    middle = None
    for n in lineNumbers:
        if n>middleNumber:
            middle = n
            break
    ret.insert(middle, "")
    return ret


if __name__ == '__main__':
    # set up file names:
    destination = 'ERD.txt'
    final_ret = ['',
            '    -- Data Base Schema  {}'.format(date),
            '    -- AKA Entity Relationship Diagram (ERD)',
            '',
            ]
    if len(sys.argv) >= 2:
        outf = sys.argv[1]
    else:
        outf = destination
    # get the data:
    schema = get_schema_with_FF()
    col1, col2 = split_on_FF(schema)
    final_ret.extend(combine(col1, col2))

    # yield the result:
    if outf:
        with open(outf, 'w') as outstream:
            outstream.write('\n'.join(final_ret))
    else:
        print('\n'.join(final_ret))

