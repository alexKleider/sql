#!/usr/bin/env python3

# File: code/ap_update.py
# ("used to be wip.py: work in progress")

"""
Developing applicant data update functions...
NOTE: there's also a wip.py file in parent directory.
AND there is code/update.py into which this code will
eventually have to be merged.
Notes:                  functions:
    application comes in      app0 or app0f
        +/- application fee   appf if app0f
    1st meeting               app1
    2nd meeting               app2
    3rd meeting               app3
    approval                  appA
    dues                      appD
    am => m (one year later)  included in appD

Still 2 do:
Need to be able to send/append letters/emails
    already handled elsewhere
Need to be able to deal with first dues payment
    already addressed
"""

import helpers
import routines
import members
import club
import content

# Some globals we might choose to change:
bcc = "alex@kleider.ca"  # string or list of strings?

def add_sponsor_data(applicant_record):
    """
    Adds the following fields to applicant_record:
    sponsor1, sponsor1email, sponsor2, sponsor2email.
    Assumes applicant_record has values for
    sponsor1ID and sponsor2ID keys.
    """
    query = """SELECT personID, first, last, suffix, email
                    FROM People
                    WHERE personID = {}; """
    # deal with each sponsor separately
    # 1st sponsor:
    res = routines.fetch(query.format(
                        applicant_record["sponsor1ID"]),
            from_file=False)
    sponsor = f"{res[0][1]} {res[0][2]}"
    suffix =  res[0][3].strip()
    if suffix: sponsor = sponsor + " " + suffix
    applicant_record['sponsor1'] = sponsor
    applicant_record['sponsor1email'] = res[0][4]
    _ = input(f"sponsor1email being assigned {res[0][4]}")
    # 2nd sponsor:
    res = routines.fetch(query.format(
                        applicant_record["sponsor2ID"]),
            from_file=False)
    sponsor = f"{res[0][1]} {res[0][2]}"
    suffix =  res[0][3].strip()
    if suffix: sponsor = sponsor + " " + suffix
    applicant_record['sponsor2'] = sponsor
    applicant_record['sponsor2email'] = res[0][4]
    _ = input(f"sponsor1email being assigned {res[0][4]}")

    return applicant_record


def applicant_record():
    """
    Returns a record with fields corresponding to all those
    in the People and the Applicants table for a current
    applicant.  Also calls add_sponsor_data (see its docstring
    above) to collect sponsors' names and emails.
    """
    print("Selecting an applicant...")
    apID = routines.pick_id()
    if apID:
#       print(f"apID: {apID}")
        rec = routines.get_rec_by_ID(apID)
        app_query = f"""
            SELECT * FROM Applicants where personID = {apID};
            """
        app_rows = routines.fetch(app_query, from_file=False)
        if len(app_rows) != 1:
            print("Not an applicant!")
            return
        app_rec = helpers.make_dict(
                routines.keys_from_schema("Applicants"),
                app_rows[0])
        for key, value in app_rec.items():
            rec[key] = value
        rec = add_sponsor_data(rec)
        print("applicant record after adding sponsor data:")
        for key, value in rec.items():
            print(f"{key}: {value}")
        return rec
    else:
        return


date_keys = [  # for each of these keys a function follows
    "app_rcvd", "fee_rcvd", "meeting1", "meeting2", "meeting3",
    "approved", "dues_paid", "notified", ]
date_keys = date_keys[:-1]  # last 2 are done both at same time
# and then each is added to a dict of functions: applicant_updates

def app0(applicant_record):
    """ No app_rcvd date: Shouldn't happen """
    print("The app_rcvd field should have been filled when")
    print("applicant was first entered into the db.")
    _ = input("Rtn to continue... ")

def appf(ap_rec):
    """ Rare that fee comes after application but possible """
    # Postpone mailing part until others are done #
    date = helpers.date_entry_w_default(
                prompt_preface="Date fee received")
    query = f"""UPDATE Applicants SET fee_rcvd = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND notified = "" AND fee_rcvd = "";"""
    print(query)
    print("Still need to update Person_Status table!")
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND statusID = 1;"""
    print(query)
    print("*** Need to GENERATE LETTER of acknowledgement***")
    #     acknowledging receipt of application
    print("...change status to 3:no meetings yet.")
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) VALUES
                ({ap_rec["personID"]}, 3, "{date}")
                ;"""
    # make Receipts entry of app fee
    query = f"""INSERT INTO Receipts
        (personID, date_received, acknowledged, ap_fee) VALUES
        ({ap_rec["personID"]}, "{date}", "{date}", 25)
        ;"""
    print(query)


def app1(applicant_record):
    """Provide credit for first meeting """
    # No need for mailing
    date = helpers.date_entry_w_default(
                prompt_preface="Date of 1st meeting")
    query = f"""UPDATE Applicants SET meeting1 = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND notified = "" AND meeting1 = "";"""
    print(query)
    print("Still need to update Person_Status table!")
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND statusID = 3;"""  # end status 3: no meetings
    print(query)
    print("... change status to 4:one meeting.")
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) values
                ({applicant_record["personID"]}, 4, "{date}")
                ;"""
    print(query)

def app2(applicant_record):
    """Provide credit for second meeting """
    # No need for mailing
    date = helpers.date_entry_w_default(
                prompt_preface="Date of 2nd meeting")
    query = f"""UPDATE Applicants SET meeting2 = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND notified = "" AND meeting2 = "";"""
    print(query)
    print("Still need to update Person_Status table!")
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND statusID = 4;"""  # end status 4: 1 meeting
    print(query)
    print("... change status to 5:two meetings.")
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) values
                ({applicant_record["personID"]}, 5, "{date}")
                ;"""
    print(query)

def app3(applicant_record):
    """Provide credit for third meeting """
    # No need for mailing
    date = helpers.date_entry_w_default(
                prompt_preface ="Date of 3rd meeting")
    query = f"""UPDATE Applicants SET meeting3 = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND notified = "" AND meeting3 = "";"""
    print(query)
    print("Still need to update Person_Status table!")
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {applicant_record["personID"]}
                AND statusID = 5;"""  # end of 2 meeting status
    print(query)
    print("...change status to 6:three meetings.")
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) values
                ({applicant_record["personID"]}, 6, "{date}")
                ;"""
    print(query)

def email(ap_rec):
    """
    <ap_rec>:an applicant record with the following fields:
        "ctype", "sponsor[1,2]email", "email"
    as well as anyting needed fo format the letter body.
    The email is created and added to club.AX_EMAIL_JSON
    defined in club module as 'Secret/ax_emails.json'.
    """
    # First prepare the email template:
    template =  ["Dear {first} {last}{suffix},"]
    template.append(ap_rec["ctype"]["body"])
    template.append(ap_rec["ctype"]["from"]["email_signature"])
    template.extend(content.get_postscripts(
                ap_rec["ctype"]) )
    ap_rec["template"] = '\n'.join(template)
    sender = ap_rec["ctype"]["from"]["email"]
    sponsors = ', '.join( [email for email in [
            ap_rec["sponsor1email"], ap_rec["sponsor2email"]]
            if email]  )
    e_rec = {
        "From": sender,
        "Sender": sender,
        "Reply-To": ap_rec["ctype"]["from"]["reply2"],
        "To": ap_rec['email'],
        "Cc": sponsors,
        "Bcc": 'alex@kleider.ca',
        "Subject": ap_rec["ctype"]["subject"],
        "attachments": [],
        "body": ap_rec["template"].format(**ap_rec),
        }
    helpers.add2json_file(e_rec, club.AX_EMAIL_JSON,
            verbose=True)


def appA(ap_rec):
    """Add board approval date """
    # Need to prepare mailing of notification & request for dues
    ap_rec["ctype"] = content.content_types[
            "request_inductee_payment"]
    prorated_dues = members.prorate(
                                helpers.month,
                                club.yearly_dues,
                                club.n_months)
    ap_rec["current_dues"] = prorated_dues
    ap_rec["ctype"] = content.content_types[
                            "request_inductee_payment"]

    date = helpers.date_entry_w_default(
                prompt_preface="Board approval date")
    query = f"""UPDATE Applicants SET approved = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND notified = "" AND approved = "";"""
    print(query)
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND statusID = 6;"""  # end 6: 3 meeting status
    print(query)
    print("Still need to send acknowledgement")
    print("*** GENERATE LETTER: voted in and fee request***")
    print("and then change status to 8:inducted & notified.")
    # If can send letters, no need for status 7
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) values
                ({ap_rec["personID"]}, 8, "{date}")
                ;"""  # membership pending payment of dues
    print(query)
    print("AND")
    query = f"""INSERT INTO Dues
                (personID, dues_owed) values
                ({ap_rec["personID"]}, {prorated_dues})
                ;"""
    print(query)
    ap_rec["ctype"] = "request_inductee_payment"
    email(ap_rec)  # files the email


def appD(ap_rec):
    """Add dues paid & became member date """
    date = helpers.date_entry_w_default(
            prompt_preface="Dues paid & notified date")
    amt_paid = int(input("Enter amount paid: "))
    # need to compare amt_paid to what's owed and continue
    # accordingly.
    res = routines.fetch(f"""SELECT dues_owed FROM Dues WHERE
                personID ={ap_rec["personID"]};""",
        from_file=False)
    owed = int(res[0][0])
    if not (int(amt_paid) == int(owed)):
        print(f"Paid: {amt_paid}; Expected: {owed}; aborting!")
        assert False   #follow a different path!
    ap_rec["ctype"] = content.content_types[
                            "welcome2full_membership"]
    email(ap_rec)
    query = f"""UPDATE Applicants SET
                    dues_paid = "{date}",
                    notified = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND notified = "" AND dues_paid = "";"""
    print(query)
    query = f"""UPDATE Person_Status set end = "{date}"
                WHERE personID = {ap_rec["personID"]}
                AND statusID = 8   -- pending receipt of dues
                ;"""
    print(query)
    print("AND")
    yr_later = int(date) + 10000
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin, end) values
                ({ap_rec["personID"]}, 11,
                "{date}", "{yr_later}")
                -- first year of membership
                ;"""
    print(query)
    print("AND")
    query = f"""INSERT INTO Person_Status
                (personID, statusID, begin) values
                ({ap_rec["personID"]}, 15, "{yr_later}")
                -- member in good standing
                ;"""
    print(query)
    print("Credit dues payment in Receipts...")
    prorated_dues = members.prorate(
                                helpers.month,
                                club.yearly_dues,
                                club.n_months)
    query = f""" INSERT INTO Receipts
                 (personID, date_received, dues, acknowledged)
                 VALUES
                 ({ap_rec["personID"]}, "{date}",
                    {prorated_dues}, "{date}")
            ;"""
    print(query)
    print("Credit dues payment in Dues...")
    query = f"""UPDATE Dues SET
                dues_owed = 0
                WHERE personID = {ap_rec["personID"]}
                    AND dues_owed = {prorated_dues}
            ;"""
    print(query)
    print("*** GENERATE LETTER: welcome to new member***")
    notices = [
        "Still need to send out receipt ....",
            ]
    for line in notices[:-1]: print(line)
    _ = input(notices[-1])


def appN(ap_rec):
    """Add 'notified of becoming a member' date """
    # No need for this; do it all in appD
    pass

applicant_updates = {
    "app_rcvd": app0,
    "fee_rcvd": appf,
    "meeting1": app1,
    "meeting2": app2,
    "meeting3": app3,
    "approved": appA,
    "dues_paid": appD,  # no need to
#   "notified": appN,   # separate these
    }

def update_applicant(applicant_record):
    """
    Calls which ever procedure is appropriate
    for the first empty date field.
    """
    for date_key in date_keys:
        if not applicant_record[date_key]:
            print(f"Need to update '{date_key}'...")
            applicant_record = add_sponsor_data(applicant_record)
            applicant_updates[date_key](applicant_record)
            show = [
                f"Ran update for '{date_key}'.",
                ]
            for line in show[:-1]:
                print(line)
                _ = input(show[:-1])
            return  # only deal with first empty date field

def select_applicant(report=None):
    helpers.add2report(report,
            "Entering code.ap_update.select_applicant...",
            also_print=True)
    # present listing of current applicants
    query = """SELECT p.personID, p.first, p.last, p.suffix,
        p.phone, p.address, p.town, p.state, p.postal_code,
        p.country, p.email,
        a.sponsor1ID, a.sponsor2ID, a.app_rcvd, a.fee_rcvd,
        a.meeting1, a.meeting2, a.meeting3,
        a.approved, a.dues_paid, a.notified
        FROM People AS p
        LEFT JOIN Applicants AS a
        ON p.personID = a.personID
        WHERE a.notified = ""
        ;   """
    while True:
        print()
        print("Listing of current applicants...")
        applicant_dicts = [dict for dict in
                routines.dicts_from_query(query)]
        IDs = [int(d['personID']) for d in applicant_dicts]
        for rec in applicant_dicts:
            rec['personID'] = int(rec['personID'])
            rec['sponsor1ID'] = int(rec['sponsor1ID'])
            rec['sponsor2ID'] = int(rec['sponsor2ID'])
#           print(rec['personID'], rec['first'], rec['last'])
            print(
              "{personID:>7}: {first:>15} {last:<15}{suffix}"
              .format(**rec))
#           print(f"\t{rec["personId"]:>3}: {rec["first"]:>3} " +
#                   f"{rec["last"]:<15}{rec["suffix"]}")
        ID = input("Pick an ID from one of the above (0 to quit): ")
        if ID == "0":
            helpers.add2report(report, "ABORTING!")
            return
        try:
            ID = int(ID)
        except TypeError:
            print("Must be an integer; try again...")
            continue
        if not ID in IDs:
            print(f"Must choose one of the IDs (or 0 to quit)...")
            continue
        else:
            print("Applicant chosen:")
            for record in applicant_dicts:
                print(f"checking {record['personID']} against {ID}")
                if record['personID'] == ID:
#                   print("Following record being returned:")
#                   for key, value in record.items():
#                       print(f"{key}: {value}")
                    return record
#           return record


def update_applicant_cmd(report=None):
    helpers.add2report(report,
            "Entering code.wip.update_applicant_cmd...")
    outfile = f"applicant_update{helpers.eightdigitdate}.txt"
    ap_rec = select_applicant(report=report)
    update_applicant(ap_rec)


def ap_mem_fee_paid():
    pass

test_rec = dict(
        apID= 231,
        personID= 231,
        first= "Josh",
        last= "McHugh",
        suffix= "",
        phone= "415/602-7873",
        address= "53 El Cerrito Ave",
        town= "San Anselmo",
        state= "CA",
        postal_code= "94960",
        country= "USA",
        email= "jcmchugh@gmail.com",
        sponsor1ID= 115,
        sponsor2ID= 65,
        sponsor1= "sponsor1",
        sponsor2= "sponsor2",
        app_rcvd= "20240828",
        fee_rcvd= "20240828",
        meeting1= "20240906",
        meeting2= "",
        meeting3= "",
        approved= "",
        dues_paid= "",
        notified= "",
        )


def ck1():
    ar = applicant_record()
    today = helpers.eightdigitdate
    for key in date_keys:
        if not ar[key]:
            try:
                new_date = input(
                    f"New date (Rtn to accept default: {today},"
                    +"\nCtl-C to quit, or"
                    +"\nenter other date): ")
            except KeyBoardInterupt:
                return
            if len(new_date) == 0:
                new_date = today
            if not (new_date.all_digits()
                and (len(new_date) == 8)):
                print(f"'{new_date}' is an invalid date.")
                pass
    if ar:
        for key, value in ar.items():
            print(f"{key}: {value}")

def ck1():
    newrec = add_sponsor_data(test_rec)
    for key, value in newrec.items():
        print(f"{key}: {value}")

def ck_func_dict():
    newrec = add_sponsor_data(test_rec)


if __name__ == "__main__":
    update_applicant_cmd()
#   ck1()

