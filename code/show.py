#!/usr/bin/env python3

# File: show.py

"""
A rewrite of the show_cmd with the (now accomplished) goal
of providing an asterix for members not yet in good standing.
(i.e. first year of membership)

Also former_members() is provided.
"""

import csv
try: import helpers, routines, commands
except ImportError: from code import helpers, routines, commands

query_files = dict(  # require formatting x2 with today' date
        applicant=      "Sql/app4join_ff.sql",
        member=         "Sql/mem4join_ff.sql",
               )       #  ^^   SQL files used ^^    #
file4web = "4web.txt"
file4app_report = "applicants.txt"


def get_listing_2f(query_file):
    """
    Returns query result.  "_2f": twice formatted
    Query is content of <query_file> formatted twice
    with today's <helper.eightdigitdate>
    """
    date = helpers.eightdigitdate
#   print(date)
    query = routines.import_query(query_file)
    query = query.format(date, date)
    #print(query)
    listing = routines.fetch(query, from_file=False)
    return listing

def member_listing():
    return get_listing_2f(query_files["member"])

def get_numbers(listing, verbose=False):
    """
    Returns a 3 tuple:
        number of first year members
        number of members in good standing
        a tuple of strings constituting a report
    """
    m0 = m1 = 0
    for item in listing:
        status = item[-1]
        if status == 11:
            m0 += 1
        elif status == 15:
            m1 += 1
        else:
            assert False, (
                "In show.py get_numbers: " +
                " member status must be 11 or 15!")

    report = (
            f"Total membership stands at {len(listing)}",
            f"of whom {m1} are 'members in good standing' while",
            f"{m0} are still within their first year of membership.",
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
        lastfield = item[-1]
        if lastfield == 11:
            prefix = '*'
        elif lastfield == 15:
            prefix = ' '
        else:
            assert False, 'Status must be 11 or 15!'
        report.append(str(prefix) +
"""{0} {1} {2} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item))
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
    n = len(listing)
    report = ['', f"Applicants (Currently {n} in number)", ]
    report.append("=" * len(report[-1]))
    previousID = 0
    for item in listing:
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
                fee_rcvd                      -- 5
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
        entry.append(f"    Applied: {app_data[5]}")
        if meetings: entry.append(meeting_line)
        report.extend(entry)
    return report

def show_applicants_cmd():
    listing = get_listing_2f(query_files["applicant"])
    report = report_applicants(listing)
    ans = input(
      f"Send applicant listing to {file4app_report}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4app_report, 'w') as outf:
            outf.write('\n'.join(report))
        report.append(
            f"Applicant listing sent to {file4app_report}.")
        print(report[-1])
    return report

def show_cmd():
    member_part = show4web(get_listing_2f(
        query_files["member"]))
    applicant_part = report_applicants(get_listing_2f(
        query_files["applicant"]))
    ret = member_part + applicant_part
    ans = input(f"Send data to {file4web}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4web, 'w') as outf:
            outf.write("\n".join(ret))
        ret.append(f"Data sent to {file4web}.")
        print(ret[-1])
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
            P.personID, P.first, P.last, P.suffix, P.email
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
        if entry[3]: entry[2] += entry[3]
        ret.append("{0:>3} {1:>10} {2:<13} {4:}".format(*entry))
    return ret


if __name__ == "__main__":
    funcs = (
        get_numbers,  # => 3 tuple: m0, m1, report
        create_membership_csv, # => memberlisting.csv
        show4web, # => list of strings: members only
        report_applicants, # => list of strings
        show_applicants_cmd, # => file.txt
        show_cmd, # => file.txt
        former_members, # => listing of strings
        )
    funcs[5]()

#   for line in show_cmd(): pass #print(line)
#   show_applicants_cmd()
#   for line in former_members(): print(line)
