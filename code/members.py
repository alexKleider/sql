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

def file_letter(holder, data):
    letter = holder.letter_template.format(**data)
    suffix = data['suffix'].strip()
    if suffix: filename = (
        f"{data['last']}_{data['first']}_{suffix}")
    else: filename = f"{data['last']}_{data['first']}"
    # indent and then file letter into MailDir
    letter = letter.split('\n')
    letter = [" "*holder.lpr['indent'] + line if line
            else line for line in letter]
    letter = '\n'.join(letter)  # LETTER HERE
    helpers.send2file(letter, 
            os.path.join(holder.mail_dir, filename))

def append_email(holder, data):
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
    holder.emails.append(email)


def q_mailing(holder, data):
    """
    Generates and dispaches email &/or letter.
    """
    data["subject"] = holder.which["subject"]
    # ^ the above should be assigned elsewhere!!
    # check how to send:
    how = holder.which["e_and_or_p"]
    if how == "email":
        append_email(holder, data)
    elif how == "both":
        append_email(holder, data)
        file_letter(holder, data)
    elif how == 'one_only':
        if data['email']:
            append_email(holder, data)
        else:
            file_letter(holder, data)
    elif how == 'usps':
        file_letter(holder, data)
    else:
        print("Problem in q_mailing: letter/email not sent to {}."
                .format(fstrings['first_last'].format(**dic)))


def dict_w_statement(dic):
    """
    Returns a new dict with 'statement' key value pair added.
    """
    dic_keys = dic.keys()
    ret_dic = {}
    for key in dic_keys:
        ret_dic[key] = dic[key]
    total = 0
    key_set = set(dic_keys)
    statement = ['Statement:',]
    if 'dues_owed' in key_set:
        total += ret_dic['dues_owed']
        statement.append("Dues...............${:3}"
                .format(ret_dic['dues_owed']))
    if 'dock' in key_set:
        total += ret_dic['dock']
        statement.append("Dock Usage fee.....${:3}"
                .format(ret_dic['dock']))
    if 'kayak' in key_set:
        total += ret_dic['kayak']
        statement.append("Kayak Storage fee..${:3}"
                .format(ret_dic['kayak']))
    if 'mooring' in key_set:
        total += ret_dic['mooring']
        statement.append("Mooring fee........${:3}"
                .format(ret_dic['mooring']))
    statement.append(    "TOTAL...................${}\n"
                .format(total))
    ret_dic['statement'] =  '\n'.join(statement)
    return ret_dic


def send_statement(holder, data):
    """
    Assumes <holder> has attribute <working_data>
    generated by the code.club.assign_owing(holder) method
    AND holder has already been set up with <which> attribute.
    <data> is data needed.
    Places letters into MailingDir
    and emails are added to holder.emails
    """
    ###### MUST ADD A statement entry to data ########
    ret = []
    w_statement = dict_w_statement(data)
#   ret.append('Running send_statements...')
    q_mailing(holder, w_statement)
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
