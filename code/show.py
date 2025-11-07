#!/usr/bin/env python3

# File: show.py

"""
A rewrite of the show_cmd with the (now accomplished) goal
of providing an asterix for members not yet in good standing.
(i.e. first year of membership)

Also former_members() is provided.

Goal still to be achieved:
    Have each function send output to a human readable file
    (such as 4web.txt, applicants.txt, etc)
    and
    option to create a CSV file of the data.
"""

import sys
import csv
try: import helpers, routines
except ImportError: from code import helpers, routines

today = helpers.eightdigitdate
file4web = f"4web{today}.txt"
file4app_report = f"applicants{today}.txt"
file4attrition = f"former_members{today}.txt"


def get_listing_2f(query_file):
    """
    Returns the result of a query that needs today's
    <helper.eightdigitdate> formatted twice.
    """
    date = today
    query = routines.import_query(query_file)
    query = query.format(date, date)
    return routines.fetch(query, from_file=False)


def modified_join_date(personID, status, jd):
    """
    Deals with special case of recent members (who where first
    year members for a year before becoming "members in good
    standing") and inactive and honorary members.
    Provides date of joining the club (when became new member)
    for people who have sinced become member in good standing.
    """
    # First deal with those who might have spent a year as
    # probatioinary members:
    if status == 15:
        res = routines.fetch(f"""SELECT begin, statusID
            FROM Person_Status
            WHERE personID = {personID}
            AND statusID = 11;""", from_file=False)
        if res:
            jd = res[0][0]
            return jd
    # Now deal with inactive and honorary members:
    if status in (14, 16):
#       print(f"dealing with memberID {personID}")
        res = routines.fetch(f"""SELECT begin, end
            FROM Person_Status WHERE
            personID = {personID} AND statusID = 15;""",
            from_file=False)
        if res:
            if res[0][0]:  # "begin" field may be empty (unknown)
                jd = res[0][0]
            else:
                jd = ''
    return jd


def get_numbers(listing, verbose=False):
    """
    Returns a 3 tuple:
        number of first year members
        number of members in good standing
        a tuple of strings constituting a report
    """
    m0 = m1 = hon = inactive = 0
    for item in listing:
        status = item[9]
        if status == 11:
            m0 += 1
        elif status in {15, 17}:
            m1 += 1
        elif status == 14:
            hon += 1
        elif status == 16:
            inactive += 1
        else:
            _ = input(f"{repr(item)}")
            assert False, (
                "In show.py get_numbers: " +
                " member status must be 11 or 15!")

    report = (
            f"Total membership stands at {m0 + m1}",
            f"of whom {m1} are 'members in good standing' while",
            f"{m0} (indicated by an (*) asterix) are still",
             "within their first year of membership.",
             "Members indicated by a (^) caret have announced",
             "their intent to retire from the club.",
            f"Also listed are {hon} honorary members, indicated by an",
            f"'at' (@) sign and {inactive} inactive members, indicated by",
             "a percent (%) sign.",
            )
    if verbose:
        for line in report:
            print(line)
    return (m0, m1, report)

def create_membership_csv(listing):
    """
    creates memberlisting.csv
    """
    fieldnames = ( "first, last, suffix, phone, address, " +
            "town, state, postal_code, email, " +
            "statusID" ).split(', ')
    outcsvfile = "memberlisting.csv"
    with open(outcsvfile, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for item in listing:
            writer.writerow(helpers.make_dict(fieldnames,item))


def show4web(listing):
    """
    Deals with members only (not applicants!)
    <listing> list of lists: [10] is begin date
    which may need modification- see modified_join_date
    """
    m0, m1, member_report  = get_numbers(listing)
    report = [f"""
FOR MEMBER USE ONLY

THE DEMOGRAPHIC DATA OF THE BOLINAS ROD & BOAT CLUB MEMBERSHIP
CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED FOR
ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BR&BC EXECUTIVE
COMMITTEE.
""",
    '\n'.join(member_report),
    f"(Last update: {helpers.date})\n", ]
    first_letter = 'A'
    for item in listing:
        last_initial = item[1][:1]
        if last_initial != first_letter:
            first_letter = last_initial
            report.append("")
        status = item[9]
        if status == 15:   # Current Member
            prefix = ' '
        elif status == 11:  # New Member (1st year)
            prefix = '*'
        elif status == 17:   # Retiring
            prefix = '^'
        elif status == 14:   # Honorary member
            prefix = '@'
        elif status == 16:   # Inactive member
            prefix = '%'
        else:
            _ = input(f"Status: {status}")
            assert False, 'Status must be 11, 15, 17, 14 or 16!'
        personID = item[-1]
        # adjust date prn
        join_date = item[10]
        join_date = modified_join_date(personID, status, join_date)
        entry = str(prefix) + """{0} {1} {2} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item)
        if join_date:
            entry = entry+" -joined: " + join_date
        report.append(entry)
    report.extend(["","", ])
    return report

newbyquery = """-- provides the applicant data
    SELECT P.personID, P.first, P.last, P.suffix,
        P.phone, P.address, P.town, P.state, P.postal_code,
        P.country, P.email,
        A.sponsor1ID, P1.first, P1.last,
        A.sponsor2ID, P2.first, P2.last,
        A.app_rcvd, A.fee_rcvd, 
        A.meeting1, A.meeting2, A.meeting3,
        A.approved, A.dues_paid
    FROM Applicants AS A
    JOIN People AS P
    ON P.personID = A.personID
    JOIN People AS P1
    ON P1.personID = A.sponsor1ID
    JOIN People AS P2
    ON P2.personID = A.sponsor2ID
    WHERE A.notified = ""
    ; """

byappstatusquery = f"""-- provides ordering and consistency ck
    SELECT P.personID, P.first, P.last, P.suffix,
        PS.statusID, S.text
    FROM People as P
    JOIN Person_Status as PS ON PS.personID = P.personID
    JOIN Stati as S on S.statusID = PS.statusID
    WHERE (PS.begin = "" or PS.begin <= {today})
        AND (PS.end = "" or PS.end > {today})
        AND PS.statusID < 11
    ORDER BY PS.statusID, P.last, P.first
    ;"""

def keysfromquery(query):
    """
    Converts "." to "_" so can be used in string formatting.
    Crashes if unsuccessful!!
    """
    ib = query.find("SELECT")
    ie = query.find("FROM")
    if ib>0 and ie>0:
        ib+= len("SELECT")
        keys = [entry.strip() for entry in
                query[ib:ie].strip().split(',')]
        keys = [key.replace(".", "_") for key in keys]
        return keys
    else:
        print("Unable to select keys from query!!!")
        sys.exit()

def show_newbie(mapping):
    """
    Assumes data came from newbyquery.
    """
    meetings = [mapping["A_meeting1"], mapping["A_meeting2"],
                mapping["A_meeting3"]]
    meetings = [meeting for meeting in meetings if meeting]
    ret = [
    """  {P_first} {P_last} {P_suffix}  {P_phone}  {P_email}
      {P_address}, {P_town}, {P_state}, {P_postal_code}
    Sponsors: {P1_first} {P1_last}, {P2_first} {P2_last}"""
           .format(**mapping), ]
    if meetings:
        ret.append("    Meetings: " +
                   ", ".join(meetings))
    return ret


def report_applicants():  # developed within try.py as "newbies()"
    """
    Returns an applicant report in the form of a sequence of strings.
    main ("newbyquery") query gets all the info we need:
    (ap_dict: a dict of dicts keyed by personID)
    while "byappstatusquery" query provides us with the order
    in which we wish to have it presented.
    (ap_stati: a listing of dicts)
    The two are compared as a consistency check!
    """
    main_keys = keysfromquery(newbyquery)
    main_keys = keysfromquery(newbyquery)
    by_status_keys = keysfromquery(byappstatusquery)
    qres1 = routines.fetch(newbyquery, from_file=False)
    n = len(qres1)
    if not n:
        return ("No applicants to report", )
    ap_dict = {}
    for line in qres1:  # all current applicant data
        ap_dict[line[0]] = {key: val for key, val  in
                            zip(main_keys, line)}
    qres2 = routines.fetch(byappstatusquery, from_file=False)
    set1 = set([entry[0:4] for entry in qres1])
    set2 = set([entry[0:4] for entry in qres2])
    if len(qres1) != len(qres2):  # concistency  check
        print("Inconsistency!!!!  The same people should")
        print("be in each of the following 2 lists... ")
        for item in qres1:
            print(item[:4])
        print()
        for item in qres2:
            print(item)
        print("!!! Could it be that none of the entries for one of")
        print("!!! the people is without an 'end' entry?????")
        _ = input("!!! Aborting execution !!!")
        sys.exit()
    if len(set1) != len(set2):     # consistency check
        print("Inconsistency!!!!  The same people should")
        print("be in each of the following 2 sets... ")
        for item in set1:
            print(item)
        print()
        for item in set2:
            print(item)
        _ = input("!!! Aborting execution !!!")
        sys.exit()
    ap_stati = [ {key: val for key, val in
                        zip(by_status_keys, line)} for line in qres2]
    subheader = ""
    report = [f"Applicants (Currently {n} in number)",]
    report.append("="*len(report[-1]))
    previousID = 0
    for mapping in ap_stati:
        if mapping["S_text"] != subheader: 
            subheader = mapping["S_text"]
            report.extend(["",
                           mapping["S_text"],
                            '-'*len(mapping["S_text"])])
        report.extend(show_newbie(ap_dict[mapping["P_personID"]]))
#       report.append(repr(ap_dict[mapping["P.personID"]]))
    return report


def show_applicants_cmd(report=None):
    helpers.add2report(report,
        "Entering code.show.show_applicants_cmd")
    ret = report_applicants()
    ret.append(
            f"\nReport generated {helpers.date}.")
    ans = input(
      f"Send applicant listing to {file4app_report}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4app_report, 'w') as outf:
            outf.write('\n'.join(ret))
        line = f"Applicant listing sent to {file4app_report}." 
        helpers.add2report(report, line)
        print(line)
    helpers.add2report(report,
        "...leaving code/show/show_applicants_cmd")
    return ret

def show_cmd(report=None):
    helpers.add2report(report,
            "Entering code.show.show_cmd", also_print=False)
    member_part = show4web(
            get_listing_2f("Sql/list4join_ff.sql"))
            # include honorary, inactive & retiring
    applicant_part = report_applicants()
    ret = member_part + applicant_part
    ans = input(f"Send data to {file4web}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4web, 'w') as outf:
            outf.write("\n".join(ret))
        line2add = f"Data sent to {file4web}."
        helpers.add2report(report, line2add, also_print=True)
        ret.append(line2add)
    helpers.add2report(report,
        "...leaving code/show/show_cmd")
    return ret


def former_members():
    """
    Returns a list of formatted strings showing
    IDs, names and emails
    of those currently in the following stati:
        18: 't'   Membership teminated
        27: 'zzz' No longer a member
        28: 'zzd' Died recently
    """
    query = """ SELECT 
            P.personID, PS.begin, P.first, P.last, P.suffix, P.email
        FROM people as P
        JOIN Person_Status as PS
        ON PS.personID = P.personID
        WHERE
            PS.statusID in (18, 27, 28)
        AND (PS.end = '' OR PS.end > {})
        AND (PS.begin = '' OR PS.begin < {})
        ORDER BY P.last, P.suffix, P.first
        ; """
    query = query.format(today,
                         today)
    res = routines.fetch(query, from_file=False)
    ret = []
    for entry in res:
        if entry[4]: entry[3] += entry[4]
        ret.append("{0:>3} {1:<8}{2:>10} {3:<13} {5:}".format(*entry))
    return ret


if __name__ == "__main__":
    funcs = (
        get_numbers,  # => 3 tuple: m0, m1, report #0
        create_membership_csv, # => memberlisting.csv #1
        show4web, # => list of strings: members only #2
        report_applicants, # => list of strings #3
        show_applicants_cmd, # => file.txt #4
        show_cmd, # => file.txt #5
        former_members, # => listing of strings #6
        )
    listing = former_members()
    for line in listing:
        print(line)
    

#   for line in show_cmd(): pass #print(line)
#   show_applicants_cmd()
#   for line in former_members(): print(line)
