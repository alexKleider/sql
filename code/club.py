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

import os.path as ospath

ROOT = "/home/alex/Git/Sql/"
DB = ospath.join(ROOT, "Secret/club.db")
db_file_name = ospath.join(ROOT, "Secret/club.db")
temp_db = ospath.join(ROOT, "Secret/temp.db")   # "/home/alex/Git/Sql/Secret/club.db"
ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"
MAIL_DIR = ospath.join(ROOT, 'Secret/MailDir')
EMAIL_JSON = ospath.join(ROOT, 'Secret/emails.json')
CONTACTS_FILE = ospath.join(ROOT, "Secret/contacts.csv")
# The above assumes one has 'exported' gmail contacts and moved
# them to the 'Secret' directory.

# the following were only for creation of DB
dock_file = ospath.join(ROOT, "Secret/dock_list.txt")
kayak_file = ospath.join(ROOT, "Secret/kayak_list.txt")
mooring_file = ospath.join(ROOT, "Secret/mooring_list.txt")


class Holder(object):

    n_instances = 0
    cc_sponsors = False
    db_file_name = db_file_name
    mail_dir = MAIL_DIR
    email_json = EMAIL_JSON
    contacts_spot = CONTACTS_FILE
    direct2json_file = False  # receipts_cmd sets it to True
    include0 = True  # include 0 balances
            # set to False if want only still owed amounts
    #  ?? Next 2 to be redacted ??
    emails = []  # list of dicts
    entries = 0  # a counter for number of receipts entered

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1

    def __init__(self):
        if self.n_instances > 0:
            raise NotImplementedError("Only one instance allowed.")
        self.inc_n_instances()

def set_include0_false(holder):
    holder.include0 = False


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


def t1():
    print('Running code/club...')
    print(f"peopleDB keys: {peopleDB_keys}")
    print(f"applicantDB keys: {applicantDB_keys}")
    print(f"meeting keys: {date_keys}")
    print(f"sponsor keys: {sponsor_keys}")
    print(f"appl keys: {appl_keys}")


if __name__ == '__main__':
    pass

