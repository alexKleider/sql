#!/usr/bin/env python3

# File: code/club.py  # contains club globals

"""
This module is specific to the Bolinas Rod and Boat Club.
Data is maintained in an SQL data base in the "Secret"
directory which (along with some other reference files) is
not part of the GIT repo but is backed up on the Club's
Google Drive. (rodandboatclub@gmail.com)
The code base is a git repository.
It provides the <Holder> class which serves largely to keep
track of Club related global values.
Allow only one instance at a time.
"""

import os.path as ospath


# ROOT = "/home/alex/Git/Sql/"
ROOT = ospath.split(ospath.dirname(ospath.realpath(__file__)))[0]
DB = ospath.join(ROOT, "Secret/club.db")
db_file_name = ospath.join(ROOT, "Secret/club.db")
temp_db = ospath.join(ROOT, "Secret/temp.db")   # "/home/alex/Git/Sql/Secret/club.db"
bu_while_testing = ospath.join(ROOT, "Secret/temp.db")
# above file stores a copy of the db prior to running tests and
# then is used to restore the db (after which it is deleted.)
ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"
MAIL_DIR = ospath.join(ROOT, 'Secret/MailDir')
EMAIL_JSON = ospath.join(ROOT, 'Secret/emails.json')
CONTACTS_FILE = ospath.join(ROOT, "Secret/contacts.csv")
LAST_REVIEW_DATE = ospath.join(ROOT, "Secret/last_review.date")
# The above assumes one has 'exported' gmail contacts and moved
# them to the 'Secret' directory.

# the following were only for creation of DB
dock_file = ospath.join(ROOT, "Secret/dock_list.txt")
kayak_file = ospath.join(ROOT, "Secret/kayak_list.txt")
mooring_file = ospath.join(ROOT, "Secret/mooring_list.txt")


class Holder(object):
    """
    A place to maintain globals pertaining to the Club.
    (The Bolinas Rod and Boat Club)
    """
    n_instances = 0
    cc_sponsors = False
    db_file_name = db_file_name
    mail_dir = MAIL_DIR
    email_json = EMAIL_JSON
    contacts_spot = CONTACTS_FILE
    direct2json_file = False  # receipts_cmd sets it to True
    #  For when add one at a time instead of
    #  storing and then dumping all at once.
    include0 = True  # include 0 balances
            # set to False if want only still owed amounts
    #  ?? Next 2 to be redacted ??
    emails = []  # List of dicts is redundant since
                 # we're using direct2json attribute.
    entries = 0  # a counter for number of receipts entered

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1
    @classmethod
    def dec_n_instances(cls):
        cls.n_instances -= 1

    def __init__(self):
        if self.n_instances > 0:
            raise NotImplementedError(
                    "Only one instance allowed.")
        self.inc_n_instances()

    def delete_instance(self):
        for key in self.__dict__.keys():
            self.__dict__[key] = None
        self.dec_n_instances()
        del self

def set_include0_false(holder):
    """
    This should be made into a method!
    """
    holder.include0 = False


## No longer need the followng ..keys tuples
## since use relational data base (SQLite3.)
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
n_months = {1:6, 2:5, 3:4, 4:3, 5:2, 6:1,
        7:12, 8:11, 9:10, 10:9, 11:8, 12:7}
# n_months: index by month of # of months remaining in Club year.

def t1():
    print('Running code/club...')
    print(f"peopleDB keys: {peopleDB_keys}")
    print(f"applicantDB keys: {applicantDB_keys}")
    print(f"meeting keys: {date_keys}")
    print(f"sponsor keys: {sponsor_keys}")
    print(f"appl keys: {appl_keys}")


if __name__ == '__main__':
    holder1 = Holder()
    print(holder1.n_instances)
    holder1.delete_instance()
    print(holder1.n_instances)
    holder2 = Holder()
    print(holder2.n_instances)


