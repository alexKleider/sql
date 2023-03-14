#!/usr/bin/env python3

# File: tests/func_tests.py

"""
Begun as a place to describe work flow.
_May_ eventually develope functional tests.
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


sqlQueries = [
'add_person_status.sql',
'applicants.sql',
'ap_stati_in_use.sql',
'changePersonStatus.sql',
'create_tables.sql',
'dropPersonStatus.sql',
'find_by_stati.sql',
'find.sql',
'forAngie.sql',
'getApplicants.sql',
'get_appl_stati_from_Stati.sql',
'get_app_stati.sql',
'get_dock_users.sql',
'get_non_member_stati.sql',
'get_stati_by_ID.sql',
'get_status_holders.sql',
'get_status_id.sql',
'meetings.sql',
'no_email.sql',
'non_member_stati.sql',
'q1.sql',
'q3.sql',
'redo_DKM_tables.sql',
'select_like.sql',
'show.sql',
'sqlite_master.sql',
'stati_contents.sql',
        ]

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
