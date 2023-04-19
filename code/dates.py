#!/usr/bin/env python3

# File: code/dates.py

"""
This module is/was for development of data entry 
that involved dates found in the following:
Person_Status: begin, end
Receipts: date_received, acknowledged
Attrition: date  (also reason)
Applicants: app_rcvd, fee_rcvd, meeting1,2,3,
            approved, dues_paid, notified
date_entry_cmd is the top level procedure which presents a menu:
    Menu choices are reflected in the tables_w_dates listing.
    These are the top level choices of this module.
"""

tables_w_dates = (
    "Applicants",    # app_rcvd, fee_rcvd, meeting1,2,3,
                     # approved, dues_paid, notified
    "Attrition",     # date  (also reason)
    "Person_status", # begin, end
    "Receipts",      # date_received, acknowledged
    )

try: from code import club
except ImportError: import club

try: from code import routines
except ImportError: import routines

try: from code import multiple
except ImportError: import multiple

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
    ret = []
    prompt = ["OK to commit the following:", ]
    f_keys = ", ".join([key for key in data.keys()])
    f_values = ", ".join([repr(value) for value in data.values()])
    prompt.extend([f_keys, f_values])
    query = ("INSERT INTO Receipts ({}) VALUES ({});"
                    .format(f_keys, f_values))
    prompt.append(query)
    yn = input('\n'.join(prompt))
    if yn and yn[0] in 'yY':
        routines.fetch(query, from_file=False, commit=True)
        ret.extend(["Query:", query, "successfully executed.",])
    else:
        ret.extend(["Query:", query, "aborted.",])
    print(ret[:-3])
    return ret

def send_acknowledgement(data, ret):
    """Sends an acknowledgement letter/email re payment""" 
    ret.extend([
"Preparing to send acknowledgement of following transaction: ",
    ])
    for key, value in data.items():
        ret.append(f"{key}: {value}")
    holder = club.Holder()
    holder.data = data
    return ret

def adjust_money_tables(data, ret):
    """Credits payments as appropriate"""
    pass

def receipts_cmd():
    """Deal with a payment."""
    ret = ["Entering receipts_cmd()", ]
    ret.append(report)
    print(ret[0])
    #1# payor?
    res = routines.id_by_name()
    print(f"The ID choice(s) is/are {res}")
    payorID = int(input("Enter ID [0 to abort]: "))
    if not (payorID and not payorID == 0):
        sys(exit)
    #2# details of the <data> to be entered
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
    ret.append(confirm_receipts_query(data, ret))
    #4# now decide if to credit accounts...
    yn = input("Credit accounts?(y/n: ")
    if not (yn and yn[0] in 'yY'):
        ret.append("Aborting receipts entry- no action takey.")
        return ret
    #4a# Crediting the accounts...
    ret.extend(multiple.credit_accounts(data))
    #5# Send letter of acknowledgement...
    yn = input("Send acknowledgement?(y/n): ")
    if not (yn and yn[0] in 'yY'):
        ret.append("Letter of acknowledgement NOT being sent.")
        return ret
    ret.extend(send_acknowledgement(data))
    return ret


def date_entry_cmd():
    ret = []
    choice = routines.get_menu_response(
        tables_w_dates, header="Which table:", incl0Q=True)
    ret.append(
        f"Your choice is #{choice}: {tables_w_dates[choice-1]}")
    if choice == 1: ret.extend(applicants_cmd())
    elif choice == 2: ret.extend(attrition_cmd())
    elif choice == 3: ret.extend(person_status_cmd())
    elif choice == 4: ret.extend(receipts_cmd())

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
            }
    print('\n'.join(send_acknowledgement(data, ret)))


if __name__ == "__main__":
    test_mailing()
#   print(date_entry_cmd())
#   observe()

