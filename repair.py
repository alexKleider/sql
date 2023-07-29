#!/usr/bin/env python

# File: repair.py

"""
Fix date entries from 8 digit to 6 digit format.
UPDATE table
SET column_1 = new_value_1,
    column_2 = new_value_2
WHERE
    search_condition1 [AND search_condition2 ...]
;
"""

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

targets_file = 'targets.txt'
targets = [targets_file, ]
fixes_file = 'fixes.txt'
fixes = [fixes_file, ]
conditions_file = 'conditions.txt'
conditions = [conditions_file, ]
files = [targets_file, fixes_file, conditions_file, ]
contents = [targets, fixes, conditions, ]
set_queries = []
set_query_format = """
            UPDATE {table} 
            SET {fix}
            WHERE
                {condition};
        """

def stringify_prn(s):
    if (isinstance(value, str)
    and not value.endswith('ID')):
        return repr(s)
    else:
        return s

def search_conditions(d):
    """
    Takes a dict parameter and
    returns an "AND" separated set of key/value pairs
    "stringifying" values pertaining to keys not ending
    in 'ID' thus producing a "AND" joined set of search
    condition for that particular SQL entry.
    IDEA: could try 'isttype' function to test for strings
    instead of assuming value of a key not ending in "ID"
    is a string.
    """
    items = []
    for key, value in d.items():
        if not key.endswith('ID'):
            d[key] = repr(value)
        items.append(f"{key} = {d[key]}")
    return " AND ".join(items)

query = "SELECT * FROM {};"

tables = ("Applicants", "Person_Status",
        "Attrition", "Receipts",)

for table in tables:
    keys = routines.get_keys_from_schema(table)
    for sequence in [targets, fixes, conditions, ]:
        sequence.append(f"\nDealing with {table} table...")
#       print(f"Keys are: {keys}")
    listing = []
    for entry in routines.fetch(query.format(table),
                                from_file=False):
        listing.append(helpers.make_dict(keys, entry))
    for d in listing:
        new_d = helpers.Rec(d)
        values2set = []
        toprint = False
        for key, value in new_d.items():
            if (isinstance(value, str)
            and value.isdecimal()
            and len(value) == 6):
                new_d[key] = repr("20" + value)
                toprint = True
                values2set.append(f"{key} = {new_d[key]}")
                # update values2set
        if toprint:
            targets.append(repr(d))
            fixes.append(', '.join(values2set))
            print("Values to set: ",end='')
            print(', '.join(values2set))
            conditions.append(search_conditions(d))
            print(search_conditions(d))
            print(f"{new_d}")
            set_queries.append(set_query_format.format(
                table=table,
                fix=fixes[-1],
                condition=conditions[-1]))
#           routines.fetch(set_queries[-1],
#                   from_file=False,
#                   commit=True)
for_testing = '''
for f, c in zip(files, contents):
    with open(f, 'w') as stream:
        stream.write("\n".join(c))
with open("queries.sql", 'w') as stream:
    stream.write("\n".join(set_queries))
'''

