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
It presents a menu reflected in the <options> listing.
Option 4: the <receipts_cmd> is currently the only one
implemented.
"""

import os
import sys
 
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


options = (  # menu below main menu item 12. Data Entry (Dates)
    "Applicants",    # app_rcvd, fee_rcvd, meeting1,2,3,
                     # approved, dues_paid, notified
    "Attrition",     # date  (also reason)
    "Person_status", # begin, end
    "Receipts",      # date_received, acknowledged
#   "Acknowledge",   # temporary to test letter preparation
    )

    
def add_date(data):
    """
    <data> a dict represention of an Applicants table row.
    Provides user with oportunity to add a date to that row &
    to update one entry and create another entry in the 
    Person_Status table.
    """
    ret = ["'add_date' being called.", ]
    keys = routines.get_keys_from_schema("Applicants")
    statusIDbyApp_key = dict(zip(keys[3:10],
                    [1, 3, 4, 5, 6, 8, 11]))
#   _ = input(f"statusIDbyApp_key: {statusIDbyApp_key}")
    query = """SELECT * from Applicants
            WHERE personID = {}
                AND notified = ''
            ; """.format(data["personID"])
    listing = routines.query2dict_listing(query, keys)
    routines.assure_only1response(listing)
    ap_data = listing[0]
    # Find first empty date field and date in field before
    # at the same time keeping track of both field names ...
    lastkey = keys[3]
    lastvalue = ap_data[keys[3]]
    for key in keys[3:10]:
        value = ap_data[key]
        if not value:
            begin = lastvalue
            newkey = key
            break
        else:
            lastkey = key
            lastvalue = value
    while True:
        print("Enter an eight digit date to serve as")
        print(f"an 'end' date for {lastkey} and")
        date2enter = input(f"a 'begin' date for {key}: ")
        if (len(date2enter) == 8) and date2enter.isdigit():
            break
    ret.append(f"added a 'date2enter' as follows: {date2enter}")
    query2check = f"""SELECT * FROM Applicants 
                WHERE personID = {data['personID']}
                    AND notified = ''
                ;"""
    res = routines.fetch(query2check, from_file=False)
    print(res[0])
    response =  input("OK to update the above record? (y/n)...")
    if not (response and response[0] in 'yY'):
        ret.append("Terminating because of failure to confirm")
        ret.append("desire to update the follwoing record:")
        ret.append(f"{response}")
        for line in ret[-3:]: print(line)
        return ret
    else:
        ret.append("Updating the record...")
#   print("variables currently in effect:")
#   print(f"keys: {keys}")
#   print(f"lastkey: {lastkey}")
#   print(f"newkey: {newkey}")
#   print(f"lastvalue: {lastvalue}")
#   print(f"date2enter: {date2enter}")
#   _ = input("Check out the above key/value pairs.")
    query0 = f"""UPDATE Applicants
                SET {newkey} = "{date2enter}"
                WHERE personID = {data['personID']}
                    AND {newkey} = ''
                    AND notified = ''
                ;"""
    query1 = f"""UPDATE PersonStatus
                SET end = "{date2enter}"
                WHERE personID = {data['personID']}
                    AND statusID = {statusIDbyApp_key[lastkey]}
                    AND begin = "{lastvalue}"
                    AND end = ''
                ;"""
    if newkey == 'dues_paid':
        pass  # need to add an end date to query2
              # and arrange query3
        yr_later = (date2enter[:3] +
                    str(int(date2enter[3]) + 1) +
                    date2enter[4:])
        print(f"yr_later calculated to be {yr_later}")
        query2 = f"""INSERT INTO Person_Status
                    (personID, statusID, begin, end)
                    VALUES (
                    {data["personID"]},
                    {statusIDbyApp_key[newkey]},
                    {date2enter},
                    {yr_later}
                    )
                    ;"""
        query3 = f"""INSERT INTO Person_Status
                    (personID, statusID, begin)
                    VALUES (
                    {data["personID"]},
                    15,
                    {yr_later}
                    )
                    ;"""
        n = 4
    else:
        query2 = f"""INSERT INTO Person_Status
                    (personID, statusID, begin)
                    VALUES (
                    {data["personID"]},
                    {statusIDbyApp_key[newkey]},
                    {date2enter}
                    )
                    ;"""
        query3 = ''
        n = 3
    print(f"Query 0: {query0}")
    print(f"Query 1: {query1}")
    print(f"Query 2: {query2}")
    if query3:
        print(f"Query 3: {query3}")
    response = input(
        f"Ok to go ahead with above {n} queries? ")
    if response and response[0] in 'yY':
        ret.append("Authorized to run commit queries!")
        print(ret[-1])
        print(f"Here's where we'd execute the {n} queries...")
        for query in (query0, query1, query2, query3):
            if query:
#               routines.fetch(query,
#                       from_file=False, commit=True)
                ret.append("Executed a commit query!")
        ret.append("Still need to run receiopt entry routine!")
        print(ret[-1])
        return ret
    else:
        ret.append("No action being taken...")
        print(ret[-1])
        return ret


def add_applicant_date():
    ret = ["Applicant date entry still under development.", ]
    print(ret[0])
    while True:
        data = routines.pick_People_record(
                header_prompt="Find an applicant...")
        if data:
            items = [(key, value, ) for key,value in data.items()]
            for key, value in items[:4]:
                line = f"{key}: {value}"
                print(line)
                ret.append(line)
            response = input("Use the above record? (yn) ")
            if response and response[0] in 'yY':
                line = "Using the above data."
                print(line)
                ret.append(line)
                break
        else:
            line = "No record found"
            print(line)
            ret.append(line)
            response = input("Abort? (y/n) ")
            if response and response[0] in 'yY':
                data = None
                break
    if data:
        ret.extend(add_date(data))
    else:
        ret.append("No suitable record found.")
    print(ret[-1])
    return ret


redact = '''
def applicants_cmd():
    """
    """
    ret = ["Applicant data entry still under development",
           "in code.data_entry module..", ]
    print('\n'.join(ret))
#   return ret
    choice = input(
        "New applicant ('yY') or just another date ('')? ")
    if choice and choice[0] in yY:
        return data_entry.add_new_applicant_cmd()
    else:
        return(add_applicant_date())
'''

def attrition_cmd():
    ret = ["Attrition entry still under development.", ]
    print(ret[0])
    return ret


def person_status_cmd():
    ret = ["Person status change still under development.", ]
    print(ret[0])
    return ret


def confirm_receipts_query(data, report=None):
    """
    If confirmed: creates a receipts entry and returns True,
    else returns None.
    If report is a list, enteries are made.
    Used by add_receipt_entries
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
        ok = True
    else:
        ret.extend(["Query:", query, "aborted.",])
        ok = False
    print(ret[-1])
    if isinstance(report, list):
        report.extend(ret)
    if ok: return True



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

    
def add_receipt_entries(holder, report=None):
    """
    Deal with a payment:
    <report> can be an existing array of strings for reporting.

    Each receipt is acknowledged by an email &/or letter.
    Letters go into holder.mail_dir and
    emails get added to already existing holder.email.json file
    both of which need to be set up by the caller <receipts_cmd>.
    Returns a negative integer: -12 if no more receipts to enter;
    -1 if unable to establish a personID; -2 abort current entry
    Returns data pertaining to entry made (which isn't used?)
    Client of confirm_receipts_query
    Used by receipts_cmd
    """
    while True:
        # Continue until get it right or quit...
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
            return
        #0# payor?
        while True:
            print("Choose a payor...")
            payorID = routines.pick_id()
            if not payorID:
                yn = input("Try again or quit (q)?: ")
                if yn and yn[0] in "qQ": return
                else: continue
            data = routines.get_demographic_dict(payorID)
            if not data:
                print(f"'{payorID}' is an invalid payorID")
                continue
            else:
                break
    ### ===  present current statement here as check yet to do !!!
        ### Check that there is something owed
        ### Could be entry of applicant fee!!
        #2# now look up all that is owed by this person
        data = routines.add_statement_data(data)
        if not data:
            print(f"No statement data available for {payorID}")
            continue
        data['before_statement'] = routines.get_statement(
                data, include_header=False)
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
            abort = False
            dues = helpers.get_int(prompt="Dues: ")
            dock = helpers.get_int(prompt="Dock usage: ")
            kayak = helpers.get_int(prompt="Kayak storage: ")
            mooring = helpers.get_int(prompt="Mooring fee: ")
            total = helpers.get_int(prompt="Total payment: ")
            if dues + dock + kayak + mooring != total:
                print("Totals don't match; try again!")
                continue
            if total == 0:
                response = input(
                    "Nothing to enter! Abort this entry? (y/n) ")
                if response and response[0] in 'yY':
                    abort = True
                    break
            break
        if abort:
            continue
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
        rep = []
        if confirm_receipts_query(data, report):
            rep.extend(multiple.credit_accounts(data))
            rep.extend(file_acknowledgement(holder, data))
            holder.entries += 1
        else:
            rep.append("Receipt entry aborted.")
            print(rep[-1])
        helpers.add2report(report, rep)
#   return data   # no idea why this line is here


def set_default_dates(holder):
    print("Enter blanks if don't want defaults...")
    holder.receipt_date = helpers.eightdigitentry(
            "Enter a default receipt date: ")
    holder.acknowledge_date = helpers.eightdigitentry(
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
    We then repeatedly call add_receipt_entries which
    1. requests an entry (personID) and
    2. data is collected
      If verified:
       i. a receipts entry is made
      ii. accounts (dues, dock, kayak, mooring) are updated.
     iii. mailing created: email or letter.
    It's up to the user to then send the emails
    and deal with the letters.
    <add_receipt_entries> needs holder as a param and also
    takes an optional param which, if provided,
    must be a list to which progress notes are added.
    Uses add_receipt_entries
    """
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
    ret.extend(content.assign_templates(holder))
    set_default_dates(holder)
    while True:
        res = add_receipt_entries(holder, ret)
        if res == None:
            ret.append("End of receipt entry.")
            print(ret[-1])
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


def date_entry_cmd(report=None):
    ret = []
    choice = helpers.get_menu_response(
        options, header="Which table:", incl0Q=True)
    ret.append(
        f"Your choice is #{choice}: {options[choice-1]}")
    if choice ==   1: ret.extend(applicants_cmd())
    elif choice == 2: ret.extend(attrition_cmd())
    elif choice == 3: ret.extend(person_status_cmd())
    elif choice == 4: ret.extend(receipts_cmd())

    helpers.add2report(report, ret, also_print=False)
    return report

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


if __name__ == "__main__":
    print("Dry run of code.dates.py")
#   test_mailing()
#   print(date_entry_cmd())
#   observe()

