#!/usr/bin/env python3

# File: code/members.py   # Note: trailing 's'.

import os

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

try: from code import club
except ImportError: import club
"""
Under old system we had a "member" (no trailing 's') module.
This will replace it for the current system.
"""


def membership():
    """
    Categories include 
        applicants
        first year members
        members in good standing
    """
    pass


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


def std_mailing_func(holder, data):
    ret = []
    ret.append('Running std_mailing_func.')
    q_mailing(holder, data) # KeyError: sponsor1ID
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

def get_email(personID):
    query = f"""SELECT email from People
            WHERE personID = {personID};"""
    res = routines.fetch(query, from_file=False)
    return res[0][0]

def exercise_get_email():
    print(get_email(112))


def sponsor2email(holder, data, email_dic):
    """
    Client is append email (where "email" is defined as a dict.
    IF holder.which specifies copies to be sent (cc or bcc):
    sorts out sponsors prn and assigns 'Cc' and 'Bcc' fields
    accordingly.
    Assumes <data> already has sponsor[1,2]ID fields.
    """
    d = {'cc': 'Cc', 'bcc': 'Bcc'}
    for copy in d.keys():
        # change 'cc' to copy 
        # change cc to recipients
        if copy in holder.which.keys():
            recipients = holder.which[copy].split(',')
            if "sponsors" in recipients:
#               _ = input(f"must [B]cc sponsors in {recipients}")
                recipients = [item for item in recipients
                        if item != 'sponsors']

                for sponsor in (data["sponsor1ID"],
                        data["sponsor2ID"]):
                    email_address = get_email(sponsor)

#               for sponsor in [data["sponsor1"],
#                       data["sponsor2"]]:
#                   email_address = data[sponsor]['email']

                    if email_address:
                        recipients.append(email_address)
            email_dic[d[copy]] = ','.join(recipients)


def append_email(holder, data):
#   print("In append_email, data holds the following:")
#   for key, value in data.items():
#       print(f"{key}: {value}")
#   _ = input()
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
    holder_keys = holder.which.keys()
    if 'cc' in holder_keys:
        sponsor2email(holder, data, email) # KeyError: sponsor1ID
    if 'bcc' in holder_keys:
        email['Bcc'] = holder.which['bcc']
    if holder.direct2json_file:
        helpers.add2json_file(email, holder.email_json,
                verbose=True)
    else:
        holder.emails.append(email)


def q_mailing(holder, data):
    """
    Generates and dispaches email &/or letter to person
    specified by <data>: is a single record based on People
    table with additional fields as needed.
    """
    print([item for item in data.items()])
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
            append_email(holder, data) # KeyError: sponsor1ID
        else:
            file_letter(holder, data)
    elif how == 'usps':
        file_letter(holder, data)
    else:
        print("Problem in q_mailing: letter/email not sent to {}."
                .format(fstrings['first_last'].format(**dic)))

def add_statement_entry(data):
    """
    <data> is a dict with dues, dock, kayak and mooring keys as
    appropriate. A 'statement' entry is added based on the above.
    """
    key_set = set(data.keys())
    statement = ['Statement:', ]
    if 'dues' in key_set:
        statement.append(f"  Dues...... ${data['dues']}")
    if 'dock' in key_set:
        statement.append(f"  Docking... ${data['dock']}")
    if 'kayak' in key_set:
        statement.append(f"  Kayak..... ${data['kayak']}")
    if 'mooring' in key_set:
        statement.append(f"  Mooring... ${data['mooring']}")
    if 'total' in key_set:
        statement.append(f"TOTAL.... ${data['total']}")
    if len(statement) > 1:
        data['statement'] = '\n'.join(statement)
    else:
        data['statement'] = "No statement available."



def dict_w_statement(dic):
    """
    Returns a new dict with 'statement' key value pair added.
    NOTE: will probably redact in favour of add_statement_entry
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


def send_acknowledgement(holder):
    """
    assigns 'payment' & 'extra' to holder.data dict
    """
    pass


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
    ret = ['Running code.members.send_statement.', ]
    add_statement_entry(data)
    if ((data['total'] == 0) and
        (not holder.include0)):
        return [
    'Total = 0: no notice sent by code.members.send_statement.',]
    q_mailing(holder, data)
    return ['Notice sent by code.members.send_statement.', ]


def inductee_payment(holder, data):
    ###### MUST ADD A 'current_dues' entry to data ########
    ret = [(
        'Requesting inductee payment for {first} {last}...'
        .format(**data)), ]
    if helpers.month > 6 or helpers.month ==1:
        data["current_dues"] = club.yearly_dues
    else:
        data["current_dues"] = club.yearly_dues/2
    q_mailing(holder, data)
    pass

# REDACT ??
def send_letter(holder, data):
    q_mailing(holder, data)


def is_new_member():
    pass


def is_dues_paying():
    pass


def thank_func(holder, data):
    """
    """
    ret = ['Running thank_func', ]
    return ret


def not_paid_up():
    pass


def is_new_applicant():
    pass


def is_inductee():
    pass


def vacancy_open():
    pass


def new_members_2b_notified():
    """
    Returns a list of dicts; each dict representing a
    People table entry for those either having status 7
    OR where the corresponding entry in the Applicant table
    has an entry for dues_paid but no entry for notified.
    """
    query = """ SELECT *
        FROM People as P
        JOIN Applicant as Ap
        ON P.personID = Ap.personID
        JOIN Person_Status as PS
        ON P.personID = PS.personID
        WHERE (Ap.notified = '' and NOT Ap.dues_paid = "")
           OR (PS.status = 7)
        ; """
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
    exercise_get_email()
#   owing_by_ID = get_owing_by_ID(None)
#   for personID in owing_by_ID.keys():
#       _ = input(get_statement(personID, owing_by_ID))

