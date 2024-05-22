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

import csv
try: import helpers, routines
except ImportError: from code import helpers, routines

file4web = f"4web{helpers.eightdigitdate}.txt"
file4app_report = f"applicants{helpers.eightdigitdate}.txt"
file4attrition = f"former_members{helpers.eightdigitdate}.txt"


def get_listing_2f(query_file):
    """
    Returns the result of a query that needs today's
    <helper.eightdigitdate> formatted twice.
    """
    date = helpers.eightdigitdate
    query = routines.import_query(query_file)
    query = query.format(date, date)
    return routines.fetch(query, from_file=False)


def member_listing():
    edd = helpers.eightdigitdate
    query = routines.import_query("Sql/mem4join_ff.sql")
    return routines.fetch(query.format(edd, edd),
            from_file=False)


def get_join_date(personID):
    """
    Provides date of joining the club (when became new member)
    for people who have sinced become member in good standing.
    """
    res = routines.fetch("""SELECT begin FROM Person_Status
        WHERE personID = {}
        AND statusID = 11;""".format(personID),
                        from_file=False)
    if res:
        return(res[0][0])

def get_numbers(listing, verbose=False):
    """
    Returns a 3 tuple:
        number of first year members
        number of members in good standing
        a tuple of strings constituting a report
    """
    m0 = m1 = 0
    for item in listing:
        status = item[9]
        if status == 11:
            m0 += 1
        elif status in {15, 17}:
            m1 += 1
        else:
            _ = input(f"{repr(item)}")
            assert False, (
                "In show.py get_numbers: " +
                " member status must be 11 or 15!")

    report = (
            f"Total membership stands at {len(listing)}",
            f"of whom {m1} are 'members in good standing' while",
            f"{m0} (indicated by an (*) asterix) are still",
             "within their first year of membership.",
             "Members indicated by a (^) caret have announced",
             "their intent to retire from the club.",
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
        if status == 11:
            prefix = '*'
        elif status == 17:
            prefix = '^'
        elif status == 15:
            prefix = ' '
        else:
            _ = input(f"Status: {status}")
            assert False, 'Status must be 11, 15 or 17!'
        personID = item[-1]
        # adjust date prn
        jd = get_join_date(personID)
        if jd: 
            item = item[:10] + (jd,) + item[11:]
        entry = str(prefix) + """{0} {1} {2} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item)
        if item[10]:
            entry = entry+" -joined: " + str(item[10])
        report.append(entry)
    report.extend(["","", ])
    return report


def get_sponsor_first_last(sponsorID):
    query = f"""SELECT first, last, suffix
            FROM People WHERE personID = {sponsorID};"""
#   _ = input(query)
    ret = routines.fetch(query,
            from_file=False)[0]
    if ret[2]: ret[1] += ret[2]
    return f"{ret[0]} {ret[1]}"


def report_applicants(listing):
    """
    <listing> as supplied by get_listing_2f()
    Flushes out sponsors and dates and orders in groups
    by number of meetings ==> a report (list of strings.)
    """
    n = len(listing)
    report = ['', f"Applicants (Currently {n} in number)", ]
    report.append("=" * len(report[-1]))
    previousID = 0
    for item in listing:
        item = list(item)
        statusID = item[-2]
        if statusID != previousID:
            previousID = statusID
            report.append(f"\n{item[-1]}")
            report.append("-" * len(report[-1]))
        if item[2]:
            item[1] += item[2]
        entry = [
"""{0} {1} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item), ]
#       print(entry)
        query = f"""SELECT
                sponsor1ID, sponsor2ID,       -- 0, 1,
                meeting1, meeting2, meeting3, -- 2,3,4
--              fee_rcvd,                     -- 5
                app_rcvd,                     -- 5
                approved                      -- 6
                FROM Applicants
                WHERE personID = {item[-3]};"""
#       _ = input(query)
        app_data = routines.fetch(query,
            from_file=False)[0]
        sponsor_line = "    Sponsors: "
        sponsors = []
        if app_data[0]:
            sponsors.append(get_sponsor_first_last(app_data[0]))
        if app_data[1]:
            sponsors.append(get_sponsor_first_last(app_data[1]))
        sponsor_line += ', '.join(sponsors)
        meeting_line = "    Meetings: "
        meetings = []
        for meeting in app_data[2:5]:
            if meeting: meetings.append(meeting)
        meeting_line += ', '.join(meetings)
        entry.append(sponsor_line)
        entry.append(f"    Applied:  {app_data[5]}")
        if meetings: entry.append(meeting_line)
        if app_data[6]: entry.append(f"    Approved: {app_data[6]}")
        report.extend(entry)
    return report

def show_applicants_cmd(report=None):
    helpers.add2report(report,
        "Entering code.show.show_applicants_cmd")
    listing = get_listing_2f("Sql/app4join_ff.sql")
    ret = report_applicants(listing)
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
            "Entering code.show.show_cmd", also_print=True)
    member_part = show4web(
            get_listing_2f("Sql/mem4join_ff.sql"))
    applicant_part = report_applicants(
            get_listing_2f("Sql/app4join_ff.sql"))
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
    query = query.format(helpers.eightdigitdate,
                         helpers.eightdigitdate)
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
