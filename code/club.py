#!/usr/bin/env python3

# File: code/club.py  # contains club globals


db_file_name = "Secret/club.db"
dock_file = "Secret/dock_list.txt"
kayak_file = "Secret/kayak_list.txt"
mooring_file = "Secret/mooring_list.txt"

ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"

people_keys = (
        "first",
        "last",
        "suffix",
        "phone",
        "address",
        "town",
        "state",
        "postal_code",
        "country",
        "email"
        )

applicant_keys = (
    "applicantID",
    "personID",
    "sponsor1",
    "sponsor2",
    "app_rcvd",
    "fee_rcvd",
    "meeting1",
    "meeting2",
    "meeting3",
    "approved",
    "inducted",
    "dues_paid",
        )

yearly_dues = 200

