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

<date_entry_cmd> is the top level procedure:
    it's driven by option 12 presented by main.py.
It presents a menu reflected in the <tables_w_dates> listing.
Option 4: the <receipts_cmd> is currently the only one
implemented.

Temporarily allow use of send_acknowledgement as a command
so it can be tested separately....
"""

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

tables_w_dates = (
    "Applicants",    # app_rcvd, fee_rcvd, meeting1,2,3,
                     # approved, dues_paid, notified
    "Attrition",     # date  (also reason)
    "Person_status", # begin, end
    "Receipts",      # date_received, acknowledged
    "Acknowledge",   # temporary to test letter preparation
    )

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
    query = ("INSERT INTO Receipts ({}) VALUES ({});"
                    .format(f_keys, f_values))
    prompt.append("Data to be added:")
    prompt.extend(  # extend method obviates need for '\n'.join
        helpers.present_listing4approval(keys, values))
    prompt.append(f"Execute: {query}")
    prompt.append("Yes or No? ")
    yn = input('\n'.join(prompt))
    ret.extend(prompt)
    if yn and yn[0] in 'yY':
        routines.fetch(query, from_file=False, commit=True)
        ret.extend(["Query:", query, "successfully executed.",])
    else:
        ret.extend(["Query:", query, "aborted.",])
    print(ret[-1])
    return ret


def file_acknowledgement(holder, data):
    """
    Assumes <holder> has 'mailing_dir', 'emails_json'
    and 'which' attributes set up.
    Adds a statement (a payment acknowledgement)to one or
    both of the above.
    """
    holder.direct2json_file = True
    ret = [
"Preparing to send acknowledgement of following transaction: ",
    ]
    ## Next 4 lines are for reporting only; not for function ##
    ret.append('<data> passed to dates.file_acknowledgement:')
    for key, value in data.items():
        ret.append(f"\t{key}: {value}")

    # add current 'statement' to data (it's assumed that the
    # payment being acknowledged is already reflected there:
    data['statement'] = routines.get_statement(
            routines.get_data4statement(data['personID']))
    # holder.emails assumed to be already set up.
    # no need for "holder_funcs": we've already got our data
    members.q_mailing(holder, data)
    ret.append("...send_acknowledgement completed.")
    return ret



def adjust_money_tables(data, ret):
    """Credits payments as appropriate"""
    pass

def get_demographic_dict(personID):
    """
    Returns a dict keyed by <keys> (see code below.)
    """
    keys = ("personID first last suffix address town " +
            "state postal_code country email")
    key_listing = keys.split()
    fields = ', '.join(key_listing)
    query = f"""
        SELECT {fields}
        FROM People 
        WHERE personID = {personID};
    """
    res = routines.fetch(query, from_file=False)
    return routines.make_dict(key_listing, res[0])

    
def add_receipt_entry(holder, ret):
    """
    Deal with a payment:
    <ret> must be an existing array of strings for reporting.

    Each receipt is acknowledged by an email &/or letter.
    Letters go into holder.mail_dir and
    emails get added to already existing holder.email.json file
    both of which need to be set up by the caller <receipts_cmd>.
    Returns a negative integer: -2 if no more receipts to enter;
    -1 if unable to establish a personID
    """
    addendum = "(add a 'd' to change dates) "
    if holder.entries:
        response = input("Enter another receipt? (y/n) "
                + addendum)
    else:
        response = input("Enter a receipt? (y/n) " 
                + addendum)
    response = set(response)
    if set('dD').intersection(response):
        set_default_dates(holder)
    if not set('yY').intersection(response):
        return -12  # signal you're done with receipt entry
    #0# payor?
    while True:
        print("Choose a payor...")
        res = routines.id_by_name()
        print(f"The ID choice(s) is/are {res}")
        try:
            payorID = int(input("Enter ID [0 to abort]: "))
        except ValueError:
            print("Must enter an integer, 0 to abort...")
            continue
        break
    if not (payorID and not payorID == 0):
        return -1  # unable to establish a payor
    #1# details of the <data> to become an entry
    data = get_demographic_dict(payorID)
#   _ = input(f"""code/dates ln#201: data..
#   {repr(data)}
#   """)
### ===  present current statement here as check yet to do !!!
    #2# now look up all that is owed by this person
    data['before_statement'] = routines.get_statement(
            routines.get_data4statement(payorID), 
            include_header=False)
    print("What's owed:")
    print(data['before_statement'])
    print("...FYI...")

    if holder.receipt_date:
        print(
          f"Using default receipt date '{holder.receipt_date}'")
        data['date_received'] = holder.receipt_date
    else:
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
            response = input("Abort this entry? (y/n) ")
            if response and response[0] in 'yY':
                return -2
        else: break
    data['total'] = total    #{ eventually to }
    data['payment'] = total  #{   be merged   }
    ## Note: only add fields if payments pertain to them:
    if dues:
        data['dues'] = dues
    if dock:
        data['dock'] = dock
    if kayak:
        data['kayak'] = kayak
    if mooring:
        data['mooring'] = mooring
    if holder.acknowledge_date:
        data["acknowledged"] = holder.acknowledge_date
        print("Using default acknowledged date " +
          f"'{holder.acknowledge_date}'")
    else:
        data["acknowledged"] = input(
                "Enter date acknowledged (YYYYMMDD): ")
    #3# receipt recorded (if confirmed)
    ret.extend(confirm_receipts_query(data))
    #4# now decide if to credit accounts...
    ## Initially steps 2 and 3 were done even if receipts
    ## entry wasn't approved; so they were broght into
    ## this function. Don't want an entry into receipts
    ## without a corresponding debit/credit to a member's
    ## account(s) _and_ a letter (or email) of
    ## acknowledgement.
    automate_vs_confirm_each_step = """
    yn = input("Credit accounts?(y/n: ")
    if not (yn and yn[0] in 'yY'):
        ret.append(
            "Receipt entry created but account not credited!")
        print(ret[-1])
        return -2
    #4a# Crediting the accounts...
    # Still assuming no one pays a fee for something for which
    # they are not registered- use <owing> dict to check
    ret.extend(multiple.credit_accounts(data))
    #5# Send letter of acknowledgement...
    yn = input("Send acknowledgement?(y/n): ")
    if not (yn and yn[0] in 'yY'):
        ret.append("Letter of acknowledgement NOT being sent.")
        return -2
    ret.extend(file_acknowledgement(holder, data))
    holder.entries += 1
    return data
    """
    ret.extend(multiple.credit_accounts(data))
    ret.extend(file_acknowledgement(holder, data))
    holder.entries += 1
    return data

def set_default_dates(holder):
    print("Enter blanks if don't want defaults...")
    holder.receipt_date = input(
            "Enter a default receipt date: ")
    holder.acknowledge_date = input(
        "Enter a default acknowledge date: ")

def receipts_cmd():
    """
    Since emails/letters are to be stacked...
    Must set up holder.email_json and MailDir...
    <holder.email_json> is created if doesn't exist;
    emails are appended. If it already exists (and not
    empty) emails are appended to what's there.
    MailDir is created if doesn't exist; letters are
    added to any that might already be there.
    Provides user with the option to set up default
    values for <date_received> and <acknowledged>.
    We then repeatedly call add_receipt_entry which
    1. requests an entry (personID) and
    2. data is collected
      If verified:
       i. a receipts entry is made
      ii. accounts (dues, dock, kayak, mooring) are updated.
     iii. mailing created: email or letter.
    It's up to the user to then send the emails
    and deal with the letters.
    <add_receipt_entry> needs holder as a param and also
    takes an optional param which, if provided,
    must be a list to which progress notes are added.
    def receipts_cmd()"""
    ret = ["Entering receipts_cmd()", ]
    holder = club.Holder()
    ## The next two functions not yet implemented:
    helpers.check_dir_exists(holder.mail_dir)
    helpers.report_if_file_exists(holder.email_json)
    ## Eliminate next part once above is implemented.
    _ = input("Check status of " +
        f"{holder.email_json} and {holder.mail_dir}")
    holder.which = content.content_types["thank"]
    holder.direct2json_file = True
    ret.extend(commands.assign_templates(holder))
    set_default_dates(holder)
    while True:
        res = add_receipt_entry(holder, ret)
        if isinstance(res, int):
            if res == -1:  # unable to establish a payor
                continue
            if res == -2:  # abort this entry only
                continue
            if res == -12:
                break
            break
        else:
            ret.append("receipt entered")
    # some cleanup is in order...
    if os.path.isdir(holder.mail_dir) and not len(
            os.listdir(holder.mail_dir)):
        yn = input(
            "Mailing directory is empty, delete it?. (y/n) ")
        if yn and yn[0] in 'yY':
            os.rmdir(holder.mail_dir)
            pass
    else:
        print("""..next steps might be the following:
    1. check and dispatch the emails (if there are any!)
    2.  $ zip -r 4Peter {0:}
        (... or using tar:
        $ tar -vczf 4Peter.tar.gz {0:}"""
            .format(holder.mail_dir))
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
    elif choice == 5: ret.extend(file_acknowledgement())
    # send_acknowledgement is temporary- 2b deleted eventually

    return ret

def observe():
    """
    ### NOT USED ###
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
    print('\n'.join(file_acknowledgement(data)))

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

