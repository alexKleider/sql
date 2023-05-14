#!/usr/bin/env python3

# File: code/dates.py

"""
This module is/was for development of data entry 
that involved dates found in the following tables:
Person_Status: begin, end
Receipts: date_received, acknowledged
Attrition: date  (also reason)
Applicants: app_rcvd, fee_rcvd, meeting1,2,3,
            approved, dues_paid, notified

<date_entry_cmd> is the top level procedure; it and it's
<receipts_cmd> is the path currently under development. 

It presents a menu reflected in the <tables_w_dates> listing.
These are the top level choices of this module.
So far only working on the receipts_cmd.
Temporarily allow use of send_acknowledgement as a command
so it can be tested separately....
"""

tables_w_dates = (
    "Applicants",    # app_rcvd, fee_rcvd, meeting1,2,3,
                     # approved, dues_paid, notified
    "Attrition",     # date  (also reason)
    "Person_status", # begin, end
    "Receipts",      # date_received, acknowledged
    "Acknowledge",   # temporary to test letter preparation
    )

import os
 
try: from code import club
except ImportError: import club

try: from code import helpers
except ImportError: import helpers

try: from code import routines
except ImportError: import routines

try: from code import content
except ImportError: import content

try: from code import members
except ImportError: import members

try: from code import multiple
except ImportError: import multiple

try: from code import commands
except ImportError: import commands

def add_new_applicant():
    ret = ["New applicant entry still under development.", ]
    print(ret[0])
    return ret
    pass

def add_applicant_date():
    ret = ["Applicant date entry still under development.", ]
    print(ret[0])
    return ret
    pass

def applicants_cmd():
    ret = ["Applicant data entry still under development.", ]
    print(ret[0])
    return ret
    choice = input(
        "New applicant ('yY') or just another date ('')? ")
    if choice and choice[0] in yY:
        add_new_applicant()
    else:
        add_applicant_date()


def attrition_cmd():
    ret = ["Attrition entry still under development.", ]
    print(ret[0])
    return ret


def person_status_cmd():
    ret = ["Person status change still under development.", ]
    print(ret[0])
    return ret


def amt_paid(text):
    """Always returns an int: zero if text is blank."""
    if not text:
        return 0
    return int(text)

def confirm_receipts_query(data):
    """
    Creates a receipts entry _if_ confirmed.
    Step #3# if confirmed
    """
    expected_keys = ("personID", "date_received", "dues",
            "dock", "kayak", "mooring", "acknowledged", )
    ret = []
    prompt = ["OK to commit the following:", ]
    keys = [key for key in data.keys()
        if key in expected_keys]
    f_keys = ", ".join(keys)
    values = [data[key] for key in keys]
    f_values = ", ".join([repr(value) for value in values])
    prompt.extend([f_keys, f_values])
    query = ("INSERT INTO Receipts ({}) VALUES ({});"
                    .format(f_keys, f_values))
    prompt.append(query)
    prompt.append("Yes or No? ")
    yn = input('\n'.join(prompt))
    if yn and yn[0] in 'yY':
        routines.fetch(query, from_file=False, commit=True)
        ret.extend(["Query:", query, "successfully executed.",])
    else:
        ret.extend(["Query:", query, "aborted.",])
    print(ret[:-3])
    return ret


def send_acknowledgement(data):
    """
    <data> key/value pairs already present:
    personID, payment, 
    .. still to be added:
    first, last, suffix, email & other demographics, and
    (a) statement (of what's being acknowledged.)
    Assumes mailing dir and emails.json are set up for additions.
    """
    ret = [
"Preparing to send acknowledgement of following transaction: ",
    ]
    ## Next 4 lines are for reporting only; not for function ##
    ret.append('<data> passed to dates.send_acknowledgement:')
    for key, value in data.items():
        ret.append(f"{key}: {value}")
    _ = input('\n'.join(ret))

    # Collect demographics and dues & fees:
    for key, value in club.get_data4statement(
            data['personID']).items():
        data[key] = value
#       print(f"{key}: {value}")
#   _ = input()
    club.add_statement(data)
    holder = club.Holder()
#   holder.working_data = [data, ]
    holder.which = content.content_types["thank"]
    ret.extend(commands.assign_templates(holder))
    # holder.emails assumed to be already set up.
    # no need for "holder_funcs": we've already got our data
    members.q_mailing(holder, data)
    # Need for this??? members.thank_func()
    pass
#   helpers.add2json_file(data, json_file, verbose=True)
    # Caller will send holder.emails_json to a json file
    # and delete mailing dir if no letters are filed:
#   helpers.dump2json_file(holder.emails, holder.email_json)
#   if os.path.isdir(holder.mail_dir) and not len(
#           os.listdir(holder.mail_dir)):
#       os.rmdir(holder.mail_dir)
#       print("Empty mailing directory deleted.")
#   else:
#       print("""..next step might be the following:
#   $ zip -r 4Peter {0:}
#   (... or using tar:
#   $ tar -vczf 4Peter.tar.gz {0:}"""
#           .format(holder.mail_dir))
    ret.append("...send_acknowledgement completed.")
    return ret



def adjust_money_tables(data, ret):
    """Credits payments as appropriate"""
    pass

    
def add_receipt_entry(holder, ret):
    """
    Deal with a payment:
    <ret> must be an existing array of strings for reporting.
    Each receipt is acknowledged by an email &/or letter.
    Letters go into holder.mail_dir and
    emails get added to already existing holder.email.json file
    both of which need to be set up by the caller <receipts_cmd>.
    ??Returns an "entry"??
    """
    if holder.entries:
        response = input("Enter another receipt? (y/n) " )
    else:
        response = input("Enter a receipt? (y/n) " )
    if not (response and response[0] in 'yY'):
        return -2  # signal you're done with receipt entry
    #1# payor?
    print("Choose a payor...")
    res = routines.id_by_name()
    print(f"The ID choice(s) is/are {res}")
    payorID = int(input("Enter ID [0 to abort]: "))
    if not (payorID and not payorID == 0):
        return -1  # unable to establish a payor
    #2# details of the <data> to become an entry
    data = {}
    data['personID'] = payorID
    #0# Should now look up all that is owed by this person
    #0# ...still to be done
    data['date_received'] = input(
            "Enter date received (YYYYMMDD): ")
    while True:
        dues = amt_paid(input("Dues: "))
        dock = amt_paid(input("Dock usage: "))
        kayak = amt_paid(input("Kayak storage: "))
        mooring = amt_paid(input("Mooring fee: "))
        total = amt_paid(input("Total payment: "))
        if dues + dock + kayak + mooring != total:
            print("Totals don't match; try again!")
        else: break
    data['total'] = total
    data['payment'] = total
    if dues:
        data['dues'] = dues
    if dock:
        data['dock'] = dock
    if kayak:
        data['kayak'] = kayak
    if mooring:
        data['mooring'] = mooring
    data["acknowledged"] = input(
            "Enter date acknowledged (YYYYMMDD): ")
    #3# receipt recorded (if confirmed)
    ret.extend(confirm_receipts_query(data))
    #4# now decide if to credit accounts...
    yn = input("Credit accounts?(y/n: ")
    if not (yn and yn[0] in 'yY'):
        ret.append(
            "Receipt entry created but account not credited!")
        print(ret[-1])
        return -2
    #4a# Crediting the accounts... (so far only dues)
    ret.extend(multiple.credit_accounts(data))
    #5# Send letter of acknowledgement...
    yn = input("Send acknowledgement?(y/n): ")
    if not (yn and yn[0] in 'yY'):
        ret.append("Letter of acknowledgement NOT being sent.")
        return -2
    ret.extend(send_acknowledgement(data))
    holder.entries += 1
    return data


def receipts_cmd():
    """
    Since emails/letters are to be stacked...
    Must set up holder.email_json and MailDir...
    We then repeatedly call add_receipt_entry which
    appends letters to the MailDir and adds a record to the
    json file defined by holder.email_json.
    It's up to the user to then send the emails
    and deal with the letters.
    <add_receipt_entry> needs hoder as a param and also
    takes an optional param which if provided must be a list
    to which progress notes are added.
    """
    helpers.check_before_deletion(
            (holder.mail_dir, holder.email_json, ),
            delete=True)
    ret = ["Entering receipts_cmd()", ]
    entries = []
    while True:
        # if we are going to keep track of entries perhaps we
        # should do it as an attribute of holder...
        entry = add_receipt_entry(holder, ret)
        if isinstance(entry, int):
            if entry == -1:  # unable to establish a payor
                continue
            break
        else:
            entries.append(entry)
            ret.append("receipt entered")
    for entry in entries:
        ret.append(repr(entry))
    return ret


def date_entry_cmd():
    ret = []
    choice = routines.get_menu_response(
        tables_w_dates, header="Which table:", incl0Q=True)
    ret.append(
        f"Your choice is #{choice}: {tables_w_dates[choice-1]}")
    if choice ==   1: ret.extend(applicants_cmd())
    elif choice == 2: ret.extend(attrition_cmd())
    elif choice == 3: ret.extend(person_status_cmd())
    elif choice == 4: ret.extend(receipts_cmd())
    elif choice == 5: ret.extend(send_acknowledgement())
    # send_acknowledgement is temporary- 2b deleted eventually

    return ret

def observe():
    """
    CREATE TABLE Receipts (
    ReceiptID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    date_received TEXT NOT NULL,
    dues INTEGER DEFAULT 0,
    dock INTEGER DEFAULT 0,
    kayak INTEGER DEFAULT 0,
    mooring INTEGER DEFAULT 0,
    acknowledged TEXT DEFAULT 0
                 --date value
    );
    """
    query = "INSERT INTO Receipts VALUES ({});"
    data = {"personID": 119,
            "date_recieved": "20230407",
            "dues": 50,
            "acknowledged": "20230410",
            }
    f_keys = ', '.join([':'+key for key in data.keys()])
    query = query.format(f_keys)
    print(query)
    pass

def test_mailing():
    ret = ['Testing acknowledgement mailing...', ]
    data = {"personID": 210,
            "date_recieved": "20230415",
            "dues": 200,
            "acknowledged": "20230417",
            "payment": 200,
            }
    print('\n'.join(send_acknowledgement(data)))

def nancy_into_receipts():
    data = {"personID": 210,
            "date_received": "20230415",
            "dues": 200,
            "acknowledged": "20230417",
            }
    print('\n'.join(confirm_receipts_query(data)))

if __name__ == "__main__":
    print("Dry run of code.dates.py")
#   nancy_into_receipts()
#   test_mailing()
#   print(date_entry_cmd())
#   observe()

