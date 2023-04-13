#!/usr/bin/env python3

# File: code/club.py  # contains club globals

"""
This module is specific to the Bolinas Rod and Boat Club.
Data is maintained in an SQL data base in a "Secret" directory
which (along with some other reference files) is not part of
the GIT repo but is backed up on the Club's Google Drive.
The code base is a git repository.
It provides the <Holder> class which serves largely to keep
track of global values.  Only one instance at a time.
"""

try: from code import routines
except ImportError: import routines

ROOT = "/home/alex/Git/Sql/"
DB = ROOT + "Secret/club.db"
db_file_name = ROOT + "Secret/club.db"
ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"
MAIL_DIR = ROOT + 'Secret/MailDir'
EMAIL_JSON = ROOT + 'Secret/emails.json'

# the following were only for creation of DB
dock_file = ROOT + "Secret/dock_list.txt"
kayak_file = ROOT + "Secret/kayak_list.txt"
mooring_file = ROOT + "Secret/mooring_list.txt"


class Holder(object):

    n_instances = 0
    cc_sponsors = False
    mail_dir = MAIL_DIR
    email_json = EMAIL_JSON

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1

    def __init__(self):
        if self.n_instances > 0:
            raise NotImplementedError("Only one instance allowed.")
        self.inc_n_instances()


## Wouldn't need the followng ..keys tuples
## if/when use sqlAlchemy
peopleDB_keys = (
    "first",         # 0
    "last",          # 1
    "suffix",        # 2
    "phone",         # 3
    "address",       # 4
    "town",          # 5
    "state",         # 6
    "postal_code",   # 7
    "country",       # 8
    "email"          # 9
    )

applicantDB_keys = (
    "applicantID",   # 0
    "personID",      # 1
    "sponsor1",      # 2
    "sponsor2",      # 3
    "app_rcvd",      # 4
    "fee_rcvd",      # 5
    "meeting1",      # 6
    "meeting2",      # 7
    "meeting3",      # 8
    "approved",      # 9
    "inducted",      #10
    "dues_paid",     #11
        )
appl_keys = (peopleDB_keys[:8] +
            peopleDB_keys[9:10]  + 
            applicantDB_keys[2:])
# not sure the next two are being used!!
date_keys = applicantDB_keys[6:10]
sponsor_keys = applicantDB_keys[2:4]

yearly_dues = 200


def assign_owing(holder):
    """
    Assigns holder.working_data dict:
    Retrieve personID for each person who owes
    putting their relevant data into a dict keyed by ID.
    """
    byID = dict()
    # dues owing:
    for tup in (routines.fetch("Sql/dues.sql")):
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'email': tup[4],
                        'address': tup[5],
                        'town': tup[6],
                        'state': tup[7],
                        'postal_code': tup[8],
                        'country': tup[9],
                        'dues_owed': tup[10],
                        }
    # dock privileges owing:
    for tup in routines.fetch("Sql/dock.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['dock'] = tup[1]
    # kayak storage owing:
    for tup in routines.fetch("Sql/kayak.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['kayak'] = tup[1]
    # mooring fee owing:
    for tup in routines.fetch("Sql/mooring.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['mooring'] = tup[1]
    # save what's been collected...
    holder.working_data = byID

def assign_welcome2full_membership(holder):
    ret = ['<welcome to full_membership mailing>',
            ]
    print("Create list of people to welcome as new member(s):")
    candidates = []
    while True:
        ids = routines.id_by_name()
        if not ids:
            break
        print('\n'.join(ids))
        print(f"Enter (coma separated if > 1) list of IDs:")
        response = input("Listing of IDs or blank to quit: ")
        if not response:
            break
        else:
            _ = input(f"Your response: {response}")
            candidates.extend([int(entry) for entry in
                                response.split(",")])
    if not candidates:  # nothing to do
        ret.append("No candidate(s) specified. Nothing to do.")
        return ret
    _ = input(f"Entries: {candidates}")
    ret.append('You chose the following: ' + ', '.join(
            [str(candidate) for candidate in candidates]))
    # run a query to populate byID ==> holder.data2welcome
    byID = dict()
    for personID in candidates:
        tup = routines.fetch('Sql/find_by_ID.sql',
                            params=(personID,))[0]
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'phone': tup[4],
                        'address': tup[5],
                        'town': tup[6],
                        'state': tup[7],
                        'postal_code': tup[8],
                        'country': tup[9],
                        'email': tup[10],
                        }
    if holder.cc_sponsors:
        for key, dic in byID.items():
            
            pass
    holder.working_data = byID
    return ret

if __name__ == '__main__':
    print('Running code/club...')
    print(f"peopleDB keys: {peopleDB_keys}")
    print(f"applicantDB keys: {applicantDB_keys}")
    print(f"meeting keys: {date_keys}")
    print(f"sponsor keys: {sponsor_keys}")
    print(f"appl keys: {appl_keys}")
