#!/usr/bin/env python3

# File: code/club.py  # contains club globals


ROOT = "/home/alex/Git/Sql/"
DB = ROOT + "Secret/club.db"
db_file_name = "Secret/club.db"
dock_file = "Secret/dock_list.txt"
kayak_file = "Secret/kayak_list.txt"
mooring_file = "Secret/mooring_list.txt"

ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"

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

if __name__ == '__main__':
    print(f"peopleDB keys: {peopleDB_keys}")
    print(f"applicantDB keys: {applicantDB_keys}")
    print(f"meeting keys: {date_keys}")
    print(f"sponsor keys: {sponsor_keys}")
