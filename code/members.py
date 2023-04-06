#!/usr/bin/env python3

# File: code/members.py   # Note: trailing 's'.

import os

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

"""
Under old system we had a "member" (no trailing 's') module.
This will replace it for the current system.

"""

redact = '''
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
'''

SEPARATOR = '|'

def get_owing_by_ID(holder):
    """
    <holder> is an instance of the code.club.Holder class
    to which is assigned the dict attribute <owing>.
    """
    query = """
    SELECT personID, dues_owed FROM Dues
    WHERE NOT dues_owed <= 0;
    """
    ret = dict()
    for personID, dues in routines.fetch(query, from_file=False):
        ret[personID] = {'Dues': dues, }

    query = """
    SELECT personID, cost FROM Dock_Privileges;
    """
    for personID, cost in routines.fetch(query, from_file=False):
        _ = ret.setdefault(personID, {})
        ret[personID]['Dock usage fee'] = cost

    query = """
    SELECT personID, slot_cost FROM Kayak_Slots;
    """
    for personID, cost in routines.fetch(query, from_file=False):
        _ = ret.setdefault(personID, {})
        ret[personID]['Kayak storage fee'] = cost

    query = """
    SELECT personID, mooring_code, mooring_cost FROM Moorings
    WHERE NOT personID = '';
    """
    for personID, code, cost in routines.fetch(
                                    query, from_file=False):
        _ = ret.setdefault(personID, {})
        ret[personID][f'Mooring ({code}) fee'] = cost
    return(ret)


def std_mailing_func(holder):
    ret = []
    ret.append('Running std_mailing_func.')
    return ret


def is_member():
    pass

def tobethanked():
    pass


def is_angie():
    pass


def testing_func(holder):
    ret = []
    ret.append('Running testing_func.')
    return ret


def bad_address_mailing_func(holder):
    ret = []
    ret.append('Running bad_address_mailing_func.')
    return ret


def letter_returned():
    pass

append_email = """  (record, club)
   body = club.email.format(**record)
    sender = club.which['from']['email']
    email = {
        'From': sender,    # Mandatory field.
        'Sender': sender,   # 0 or 1
        'Reply-To': club.which['from']['reply2'],  # 0 or 1
        'To': record['email'],  # 1 or more, ',' separated
        'Cc': '',             # O or more comma separated
        'Bcc': '',            # O or more comma separated
        'Subject': club.which['subject'],  # 0 or 1
        'attachments': [],
        'body': body,
    }
    sponsor_email_addresses = []
    if club.cc_sponsors:
        record = helpers.Rec(record)
        name_key = record(fstrings['key'])
        if name_key in club.applicant_set:
            sponsors = club.sponsors_by_applicant[name_key]
            for sponsor in club.sponsors_by_applicant[name_key]:
                keys = club.sponsor_emails.keys()
                if sponsor in set(club.sponsor_emails.keys()):
                    sponsor_email_addresses.append(club.sponsor_emails[sponsor])
            emails_set = set(sponsor_email_addresses)
            club.cc = club.cc.union(set(sponsor_email_addresses))
            club.cc = club.cc.difference({''})
    email['Cc'] = ','.join(club.cc)
    if club.bcc:
        email['Bcc'] = club.bcc
    club.json_data.append(email)
"""

file_letter = """
    entry = club.letter.format(**record)
    path2write = os.path.join(club.MAILING_DIR,
                              "_".join((record["last"],
                                        record["first"]))
                              + '.txt')
    with open(path2write, 'w') as file_obj:
        file_obj.write(helpers.indent(entry,
"""

q_mailing = """
   record["subject"] = club.which["subject"]
    # ^ the above should be assigned elsewhere!!
    # check how to send:
    how = club.which["e_and_or_p"]
    if how == "email":
        append_email(record, club)
    elif how == "both":
        append_email(record, club)
        file_letter(record, club)
    elif how == 'one_only':
        if record['email']: 
            append_email(record, club)
        else:
            file_letter(record, club)
    elif how == 'usps':
        file_letter(record, club)
    else:
        print("Problem in q_mailing: letter/email not sent to {}."
                .format(fstrings['first_last'].format(**record)))

"""

std_mailing = """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        if club.owing_only:
            if record['owing']:
                q_mailing(record, club)
        else:
            q_mailing(record, club)
"""

def send_statement(holder, data):
    """
    Assumes <holder> has attribute <working_data>
    generated by the code.club.assign_owing(holder) method
    AND holder has already been set up with <which> attribute.
    <data> is data needed.
    Places letters into MailingDir
    and emails are added to holder.emails
    """
    ret = []
#   ret.append('Running send_statements...')
    letter = holder.letter_template.format(**data)
    suffix = data['suffix'].strip()
    if suffix: filename = (
        f"{data['last']}_{data['first']}_{suffix}")
    else: filename = f"{data['last']}_{data['first']}"
#   _ = input(f"filename: {filename}")
    # indent and then file letter into MailDir
    letter = letter.split('\n')
    letter = [" "*holder.lpr['indent'] + line if line
            else line for line in letter]
    letter = '\n'.join(letter)
############ uncomment next 2 lines ############
#   helpers.send2file(letter, 
#           os.path.join(holder.mail_dir, filename))
    if "Kleider" in filename:
        helpers.send2file(letter, 
            os.path.join(holder.mail_dir, filename))
    email_body = holder.email_template.format(**data)
#   =========================
    sender = holder.which['from']['email']
    email = {
        'From': sender,    # Mandatory field.
        'Sender': sender,   # 0 or 1
        'Reply-To': holder.which['from']['reply2'],  # 0 or 1
        'To': data['email'],  # 1 or more, ',' separated
        'Cc': '',             # O or more comma separated
        'Bcc': '',            # O or more comma separated
        'Subject': holder.which['subject'],  # 0 or 1
        'attachments': [],
        'body': email_body,
    }
    sponsor_email_addresses = []
    forLater = """
    if holder.cc_sponsors:
        record = helpers.Rec(record)
        name_key = record(fstrings['key'])
        if name_key in club.applicant_set:
            sponsors = club.sponsors_by_applicant[name_key]
            for sponsor in club.sponsors_by_applicant[name_key]:
                keys = club.sponsor_emails.keys()
                if sponsor in set(club.sponsor_emails.keys()):
                    sponsor_email_addresses.append(club.sponsor_emails[sponsor])
            emails_set = set(sponsor_email_addresses)
            club.cc = club.cc.union(set(sponsor_email_addresses))
            club.cc = club.cc.difference({''})
    email['Cc'] = ','.join(club.cc)
    if club.bcc:
        email['Bcc'] = club.bcc
    """
#   holder.emails.append(email)
    if 'kleider' in data['email']:
        holder.emails.append(email)
    return ret


def is_dues_paying():
    pass


def thank_func(holder):
    ret = ['Running thank_func', ]
    return ret


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

def get_statement(personID, byID):
    query = """SELECT first, last, suffix FROM People
    WHERE personID = ?;
    """
    first, last, suffix = routines.fetch(query,
            from_file=False, params=(personID, ))[0]
    total = 0
    statement = [f'Statement (for {first} {last}) as of {helpers.date}', ]
    for item, cost in byID[personID].items():
        total += cost
        statement.append(f"{item:>20}: ${cost}")
    statement.append(f"                 TOTAL:  ${total}")
    return '\n'.join(statement)


if __name__ == '__main__':
    owing_by_ID = get_owing_by_ID(None)
    for personID in owing_by_ID.keys():
        _ = input(get_statement(personID, owing_by_ID))
