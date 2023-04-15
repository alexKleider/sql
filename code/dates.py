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
    # payor?
    res = routines.id_by_name()
    print(f"The ID choice(s) is/are {res}")
    payorID = int(input("Enter ID [0 to abort]: "))
    if not (payorID and not payorID == 0):
        sys(exit)
    while True:
        dues = amt_paid(input("Dues: "))
        dock = amt_paid(input("Dock usage: "))
        kayak = amt_paid(input("Kayak storage: "))
        mooring = amt_paid(input("Mooring fee: "))
        total = amt_paid(input("Total payment: "))
        if dues + dock + kayak + mooring != total:
            print("Totals don't match; try again!")
        else: break
    # date paid
    date_received = input("Enter date received (YYYYMMDD): ")
    # date acknowledged
    date_acknowledged = input(
            "Enter date acknowledged (YYYYMMDD): ")
    prompt = ["OK to commit the following:", ]
    if dues: prompt.append( f"  Dues..........{dues:>3}")
    if dock: prompt.append( f"  Dock usage....{dock:>3}")
    if kayak: prompt.append(f"  Kayak storage.{dock:>3}")
    if dock: prompt.append( f"  Mooring fee...{dock:>3}")
    prompt.append(          f"  TOTAL............${total:>3}")
    response = input("Y/N?.. ")
    if response and response[0] in 'yY':
        ret.append("Processing the following:")
        for line in prompt[1:]:
            ret.append(line)
        print('\n'.join(ret[:-5]))
    query = """
    """
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

if __name__ == "__main__":
    print(date_entry_cmd())

