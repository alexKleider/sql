#!/usr/bin/env python3

# File: code/data_entry.py

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

try: from code import textual
except ImportError: import textual

try: from code import club
except ImportError: import club

"""
Handle adding data to the db.
An ammalgamation of what used to be applicants.py
and update.py

Provides
    data_entry.add_new_applicant_cmd()
    data_entry.change_status_cmd() (under development)
    data_entry.applicant_update_cmd() (under development)
"""
app_query = """ -- current applicants
    SELECT P.personID, P.last, P.first, P.suffix,
        A.sponsor1ID, A.sponsor2ID, A.app_rcvd, A.fee_rcvd,
        A.meeting1, A.meeting2, A.meeting3, approved,
        dues_paid, notified
    FROM People as P JOIN Applicants as A
    WHERE A.personID = P.personID
    AND A.notified = "";"""

def add2tables(data, report=None):
    """
    One time use for each new applicant.
    <data> is a dict created based on an application.
    Entries need to be made into the following tables:
    People: demographics
    Person_Status: 1. no fee, 2. fee paid, (3. acknowledged (a0))
    Applicants: sponsor1ID, sponsor2ID, app_rcvd, fee_rcvd
    Yet to add: (to be done in add2tables!!!)
        a. if ap_fee paid- Enter into Receipts
        c. Send welcoming email
        b. End status 2 and begin status 3
    """
    helpers.add2report(report, "Entering add2tables...",
            also_print=True)
    # <data> is all that's needed for a People table entry
    # Only after that's done can we find out the personID
    # data for Person_Status table:
    all_keys = [key for key in data.keys()]
    key_params = ', '.join(all_keys[:10])
    all_values =  [value for value in data.values()]
    # all values to be entered into People table are text:
    val_params = '"' + '", "'.join(all_values[:10]) + '"'
    people_insert_query = f"""
    INSERT INTO People ({key_params})
    VALUES ({val_params})
    ;"""
    print('\n' + people_insert_query)
    yn = input(
        f"OK to commit the query shown above?: (y/n): ")
    if yn and yn[0] in 'Yy':
        res = routines.fetch(people_insert_query,
                from_file=False,
                commit=True, verbose=True)
        helpers.add2report(report, 
                "...successfull addition to People table.",
                also_print=True)
        # Need to retrieve newly assigned personID...
        res = routines.fetch_d_query("Sql/id_from_names_fd.sql",
                data)
        data['personID'] = res[0][0]
        print(f"New personID is {data['personID']}")
    else: 
        helpers.add2report(report, "...borting add2tables!",
                            also_print=True)
        return

    # Set data needed and then make the Person_Status entry...
    if data["fee_rcvd"]:
        fee_rcvd = True
        #### WORK HERE ####
        ## good place to make entry into Receipts table ##
        # .. use data['personID']
        data['statusID'] = 2
        data['begin'] = data['fee_rcvd']
    else:
        fee_rcvd = False
        data['statusID'] = 1  # Will have to add an end date
                        # and make another status entry
                        # when fee is paid.
        data['begin'] = data['app_rcvd']
    _ = routines.fetch_d_query(
            "Sql/person_status_entry_fd.sql", data, commit=True)
    # Finally create entry in Applicants table...
    _ = routines.fetch_d_query(
            "Sql/applicant_entry_fd.sql", data, commit=True)
    if fee_rcvd:
        # make entry into Receipts table...
        query = f"""INSERT INTO Receipts
               (personID, date_received, acknowledged, ap_fee)
            VALUES (data['personID'], "{data['fee_rcvd']}",
                "{helpers.eightdigitdate}", club.applicant_fee);
        """
        print("Go ahead with the following query...")
        print(query)
        yn = input("OK? (y/n): ")
        if yn and yn[0] in 'Yy':
            routines.fetch(query, from_file=False, commit=True)
    helpers.add2report(report, [
            "{first} {last} {suffix} added as new applicant."
                .format(**data),
            "Tables updated: People, Person_Status & Applicants.",
            "Still need to...",
            "  mail welcome letter (mailing menu #20),",
            "  update status from 2 to 3,",
            "& create entry in gmail contacts.",
            "Then check for data consistency.",
            ], also_print=True)


def file2app_data(file_content, report=None):
    """
    Returns a dict with keys relevant to new applicants.
    <file_content> must refer to text read from a file having
    one line for each (except the first) field present in the
    'People' table schema followed by a line each for sponsor1,
    sponsor2, date application was received and date fee was
    received (enter '0' if fee did not accompany the application.
    Note: Sponsors in the source are by three names (first, last,
    suffix) and a date (which is not used)
    but the code translates these into personID numbers.
    """
    data = [line for line in helpers.useful_lines(
                            file_content)]
#   _ = input(f"data collected from file:\n{data}")
    keys = routines.keys_from_schema(
                    'People', brackets=(1,0))
    keys.extend(
        ['sponsor1ID', 'sponsor2ID', 'app_rcvd', 'fee_rcvd'])
#   _ = input(f"keys collected from file:\n{keys}")
    ret = dict(zip(keys, data))
#   _ = input(f"Resulting dict:\n{ret}")
    if ret['suffix'] == 'No Suffix': ret['suffix'] = ''
    if ret['app_rcvd'] == 0: ret['app_rcvd'] = ''
    if ret['fee_rcvd'] == 0: ret['fee_rcvd'] = ''
    with open("Sql/id_from_names_fd.sql", 'r') as inf:
        query = inf.read()
    for sponsor in ('sponsor1ID', 'sponsor2ID'):
        tup = ret[sponsor].split()
        l = len(tup)
        d = {"first": tup[0], "last": tup[1], "suffix": ''}
        if l == 4:
            d["suffix"] = tup[2]
        res = routines.fetch_d_query(
                "Sql/id_from_names_fd.sql", data=d)
#       _ = input(f"fetch_d_query on {d} returning {res}")
        ret[sponsor] = res[0][0]
    helpers.add2report(report,
        f"file2app_data() called on\n{file_content}")
    if (not (len(data) == len(keys))):
        helpers.add2report(report,
            "Lengths don't match.",also_print=True)
    helpers.add2report(report, 
            f"file2app_data returning:\n{ret}",
            also_print=True)
    return ret  # returns dict of new applicant data from file


def add_new_applicant_cmd(report=None):
    """
    Provides ability to enter one new applicant into the db:
    Creats appropriage entries in "People", "Person_Status"
    and "Applicant" tables. 
    Yet to add: (to be done in add2tables!!!)
        a. if ap_fee paid- Enter into Receipts
        c. Send welcoming email
        b. End status 2 and begin status 3
    Returns a report (in the form of a list of lines.)
    """
    if not report: report=[]
    helpers.add2report(report,
                        "Entering add_new_applicant_cmd...",
                        also_print=True)
    data = textual.get_demographics(report=report)
    if not data: 
        helpers.add2report(report,
                        "...add_new_applicant aborted",
                        also_print=True)
        return
    routines.add_sponsorIDs(data)
    add2tables(data, report=report)  # adds to three tables:
            #1. People
            #2. Person_Status
            #3. Applicants
    return report


def choose_applicant(report=None):
    """
    Offers a menu/choice of all current applicants.
    Returns a dict representing chosen applicant
    OR None if no choice made (possibly no applicants.)
    """
    helpers.add2report(report,
            "Entering 'choose_applicant' function...",
            also_print=True)
    # first query current applicants...
    res = routines.query2dict_listing(app_query,
        routines.keys_from_query(app_query), from_file=False)
    n_res = len(res)
    helpers.add2report(report,
        f"...found {n_res} applicants from which to choose...",
        also_print=True)
    if n_res == 0: return  # return None if no applicants
    # set up mapping for the menu function
    mapping = {}
    for entry in res:
        if entry['suffix']: suffix = f' [{suffix.strip()}]'
        else: suffix = ''
        key = (f'{entry["personID"]:>4d} {entry["last"]}, '
            + f'{entry["first"]}' + suffix)
#       limited_entry = {}
#       for k in date_keys:
#           limited_entry[k] = entry[k]
#       mapping[key] = limited_entry
        mapping[key] = entry
    helpers.add2report(report,
        "...returning from 'choose_applicant' function.")
    # use menu function to choose (and return) applicant
    applicant = textual.menu(mapping, report=report,
            headers=["Current Applicants", "Pick an applicant"])
    if applicant:
        print("Applicant chosen: {personID:>3d} {last}, {first}"
            .format(**applicant))
    return applicant


def get_key_val2change(mapping, report=None):
    """ moved into code/data_entry
    Presents a dialog box containing <mapping>'s key/value pairs.
    Returns a mapping of any key/value pairs that were changed...
    or None if nothing changed or user "CANCEL"s.
    """
    if not mapping: # { choose_applicant
        return        # { might return None
    helpers.add2report(report,
        "Entering 'get_key_val2change' function...",
        also_print=True)
    ret = textual.change_or_add_values(mapping,
        report=report,
        headers=["Applicant Data", "Change or add an item..."])
    if not ret:
        helpers.add2report(report,
            "...'get_key_val2change' returning None.",
            also_print=True)
        return
#   helpers.print_key_value_pairs(mapping)
#   helpers.print_key_value_pairs(ret)
    changes = {}
    for key in mapping.keys():
        if str(mapping[key]) != str(ret[key]):
#           print(f"{key}: '{mapping[key]}' != '{ret[key]}'")
            changes[key] = ret[key]
    if changes:
        helpers.add2report(report,
            "...'get_key_val2change' returning changes.",
            also_print=True)
        return changes
    else:
        helpers.add2report(report,
            "...'get_key_val2change' made no changes",
            also_print=True)


def query2update_applicant_table(personID, mapped_changes,
                            report=None):
    """
    Returns a query to update the Applicant table.
    """
    # Could be a re-application...
    entries = routines.query2dict_listing(
            f"""SELECT * FROM Applicants
            WHERE personID = {personID};""",
            routines.keys_from_schema("Applicants"))
    if len(entries) > 1:
        helpers.add2report(report,
            "More than one entry for this applicant!",
            also_print=True)
    app_rcvd = entries[-1]["app_rcvd"]
    # ...so pick the most recent entry
    query = f"""UPDATE Applicants SET
            {{}}
            WHERE personID = {personID}
            AND app_rcvd = {app_rcvd}
            ;"""
    entries = ', '.join([f"{key} = {value}" for key, value in
            mapped_changes.items()])
    query = query.format(entries)
    return query

def update_applicant_date_cmd(report=None):
    """
    Choice of applicants,
    Current entries for applicant chosen with option to change,
    confirm and execute changes to Applicant table
    confirm and execute update to Person_Status table
    confirm and execute new entry to Person_Status table
    """
    helpers.add2report(report,
            "Enterning update_applicant_date_cmd...",
            also_print=True)
    chosen_applicant = choose_applicant(report)
    if not chosen_applicant:
        helpers.add2report(report,
            "Choosing an applicant was aborted.",
            also_print=True)
        return
    personID = chosen_applicant["personID"]
    changes = get_key_val2change(chosen_applicant, report)
    if changes:
        dates = [change for change in changes.values()]
        new_date = dates[0]
        query = query2update_applicant_table(personID,
                changes, report)
        if textual.yes_no(query,
                title="Execute query?"):
            routines.fetch(query, from_file=False,
                            commit=True, verbose=True)
            helpers.add2report(report,
                ["Following query has been executed:", query],
                                            also_print=True)
        else:
            helpers.add2report(report,
                    "Aborting applicant table update.",
                    also_print=True)
            return
    else:
        helpers.add2report(report,
                'No applicant changes to be made.',
                also_print=True)
        return
    
    # here's where we can change the Person_Status Table:
    person = "{personID:>3d}: {last}, {first}{suffix}".format(
            **chosen_applicant)
#   _ = input(chosen_applicant)
    # first pick the entry to update:
    picked = textual.pick(
        f"""SELECT P.personID, P.last, P.first, P.suffix,
            Ps.statusID, PS.begin, PS.end 
        FROM Person_Status AS PS
        JOIN People AS P
        WHERE P.personID = PS.personID
        AND P.personID = {chosen_applicant['personID']};""",
        ("{personID:>3d} {last}, {first} {suffix}" +
        " {statusID} {begin} {end}"),
        header="Choose Status Entry to Update",report=report)
    helpers.add2report(report,
        ["applicant_update_cmd 1st status change picked:",
        repr(picked)], also_print=True)
    picked["new_date"] = new_date
    # TypeError: 'NoneType' object does not support item assignment
    update_query = """UPDATE Person_Status SET 
        end = "{new_date}" WHERE personID = {personID}
        AND statusID = {statusID}
        AND end = "";""".format(**picked)
    helpers.add2report(report,
        [f"1st (update) query:", repr(update_query)],
        also_print=True)
    if textual.yes_no(update_query,
            title="Execute query?"):
        routines.fetch(update_query, from_file=False,
                        commit=True, verbose=True)
        helpers.add2report(report, 
            ["Following update_query executed:", update_query],
                also_print=True)
    # next set up for new status entry:
    picked["statusID"] = int(picked["statusID"]) + 1
    # ^ we are assuming that new statusID incriments by 1^
    insert_query = """INSERT INTO Person_Status
        (personID, statusID, begin)
        VALUES
        ({personID}, {statusID}, "{new_date}");
        """.format(**picked)
    helpers.add2report(report,
        [f"2nd (insert) query:", insert_query],
        also_print=True)
    if textual.yes_no(insert_query,
            title="Execute query?"):
        routines.fetch(insert_query, from_file=False,
                        commit=True, verbose=True)
        helpers.add2report(report,
            ["Following insert_query executed:",
                insert_query],
                also_print=True)
    yn = input("Show report? y/n: ")
    if yn and yn[0] in "yY":
        for line in report:
            print(line)
    

def change_status_cmd(report=None):
    """
    """
    if not report:
        report = []
    helpers.add2report(report, 
            "Entering code/data_entry/change_status_cmd...",
            also_print=True)
    # 1st pick a person record ==> data:
    data = textual.selectP_record(report=report)
    if not data:
        helpers.add2report(report,
            "code/data_entry/selectP_record " +
            "failed to return a record",
            also_print=True)
        return
    else:
        helpers.add2report(report,
            "<data> now contains a People table entry",
#           also_print=True)
            also_print=False)
    # Get the person's ID:
    personID = data['personID']
    # Collect person's entries in the Person_Status table
    stati = routines.dicts_from_query(
        f"""SELECT * FROM Person_Status WHERE
        personID = {personID};""")
    if not stati:
        helpers.add2report(report,
            "... aborting change_status.cmd")
        return
    for mapping in stati:
        print(repr(mapping))
    helpers.add2report(report,
        "...finished code/data_entry/change_status.cmd.",
        also_print=True)
    return report


def applicant_update_cmd():
    """
    """
    report = ["Entering applicant_update_cmd...", ]
    report.extend(["under development....",
            "Leaving applicant_update_cmd",])
    return report


def test_add_new_applicant_cmd():
    for line in add_new_applicant_cmd():
        print(line)

if __name__ == "__main__":
    report = [
        "Running update_applicant_date_cmd from within " +
        "code/data_entry.py", ]
    update_applicant_date_cmd(report = report)
    for line in report:
        print(line)
#   test_add_new_applicant_cmd()

