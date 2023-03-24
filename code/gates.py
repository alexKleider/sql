#!/usr/bin/env python3

# File: code/gates.py

"""
supports mailing functions
selects persons who should receive mail

May redact this module in favour of putting this
all into the members module.
"""

try: from code import routines
except ImportError: import routines

def members_only(fields_wanted=('P.personID', )):
    """
    Returns a listing of tuples:
        fields specified (for members only.)
    Default is to return only personID.
    """
    query = """ /* listing of members */
        SELECT  -- needs to be formatted
            {}
        FROM People AS P
        JOIN Person_Status AS PS
        ON P.personID = PS.personID
        JOIN Stati as St
        ON St.statusID = PS.statusID
        WHERE St.key = 'm'
        ;
        """
    query = query.format(', '.join(fields_wanted))
#   _ = input(query)
    return routines.fetch(query, from_file=False)

if __name__ == '__main__':
    print("Running code/gates.py")
    res = members_only(fields_wanted =(
        'P.personID', 'first', 'last',))
    n = len(res)
    for member in res:
        print(member)
    print(f"Number of members: {n}")
