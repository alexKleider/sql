#!/usr/bin/env python3

# File: code/members.py   # Note: trailing 's'.

"""
Under old system we had a "member" (no trailing 's') module.
This will replace it for the current system.

"""

STATUS_KEY_VALUES = {   # Hope this can be redacted
                        # or if not, than moved to 'club' module.
    "a-": "Application received without fee", #0
    "a" : "Application complete but not yet acknowledged",
                # temporary until letter of welcome is sent
    "a0": "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ai": "Inducted, needs to be notified",  # temporary until letter
    "ad": "Inducted & notified, membership pending payment of dues",
    "av": "Vacancy ready to be filled pending payment of dues",
    "aw": "Inducted & notified, awaiting vacancy", #7 > #8
    "am": "New Member",  # temporary until congratulatory letter.
    "be": "Email on record being rejected",   # => special notice
    "ba": "Postal address => mail returned",  # => special notice
    "h" : "Honorary Member",                             #10 > #12
    'm' : "Member in good standing",
    'i' : "Inactive (continuing to receive minutes)",
    'r' : "Retiring/Giving up Club Membership",
    't' : "Membership terminated (probably non payment of fees)",
            # a not yet implemented temporary
            # status to trigger a regret letter
    "w" : "Fees being waived",  # a rarely applied special status
    'z1_pres': "President",
    'z2_vp': "VicePresident",
    'z3_sec': "Secretary of the Club",
    'z4_treasurer': "Treasurer",
    'z5_d_odd': "Director- term ends Feb next odd year",
    'z6_d_even': "Director- term ends Feb next even year",
    'zae': "Application expired or withdrawn",
    'zzz': "No longer a member"  # not implemented
            # may use if keep people in db when no longer members
    }

SEPARATOR = '|'


def std_mailing_func():
    pass


def is_member():
    pass

def is_angie():
    pass


def testing_func():
    pass


def bad_address_mailing_func():
    pass


def letter_returned():
    pass


def assign_statement2extra_func():
    pass


def is_dues_paying():
    pass


def thank_func():
    pass


def not_paid_up():
    pass


def is_new_applicant():
    pass


def is_inductee():
    pass


def inductee_payment_f():
    pass


def vacancy_open():
    pass


def is_new_member():
    pass


def is_terminated():
    pass

