#!/usr/bin/env python3

# File: code/dates.py

"""
Person_Status: begin, end
Receipts: date_received, acknowledged
Attrition: date  (also reason)
Applicants: app_rcvd, fee_rcvd, meeting1,2,3,
            approved, dues_paid, notified
"""

tables_w_dates = (
    "Applicants",    # app_rcvd, fee_rcvd, meeting1,2,3,
                     # approved, dues_paid, notified
    "Attrition",     # date  (also reason)
    "Person_status", # begin, end
    "Receipts",      # date_received, acknowledged
    )

try: from code import routines
except ImportError: import routines

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

def applicants():
    ret = ["Applicant data entry still under development.", ]
    print(ret[0])
    return ret
    choice = input(
        "New applicant ('yY') or just another date ('')? ")
    if choice and choice[0] in yY:
        add_new_applicant()
    else:
        add_applicant_date()


def attrition():
    ret = ["Attrition entry still under development.", ]
    print(ret[0])
    return ret
    pass

def person_status():
    ret = ["Person status change still under development.", ]
    print(ret[0])
    return ret
    pass

def amt_paid(text):
    if not text:
        return 0
    return int(text)

def receipts():
    ret = []
    report = "entering receipts()"
    ret.append(report)
    print(report)
    # payor?
    res = routines.id_by_name()
    print(f"The ID choice(s) is/are {res}")
    payorID = int(input("Enter ID [0 to abort]: "))
    if not (payorID and not payorID == 0):
        sys(exit)
    data = {}
    data['personID'] = payorID
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
    return ret


def date_entry_cmd():
    ret = []
    choice = routines.get_menu_response(
        tables_w_dates, header="Which table:", incl0Q=True)
    ret.append(
        f"Your choice is #{choice}: {tables_w_dates[choice-1]}")
    if choice == 1: applicants()
    elif choice == 2: attrition()
    elif choice == 3: person_status()
    elif choice == 4: receipts()

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


if __name__ == "__main__":
    print(date_entry_cmd())
#   observe()

