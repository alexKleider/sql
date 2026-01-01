#!/usr/bin/env python3

# File: exec.py

"""
Print up a report for the exec committee.
"""

from code import helpers
from code import show
from code import club

def report_cmd(report=None):
    helpers.add2report(report,
        "Entering code.commands.report_cmd...")
    outfile = f"report{helpers.eightdigitdate}.txt"
#   n = len(show.member_listing())
    n = len(show.get_listing_2f("Sql/mem4join_ff.sql"))
    ret = []
    helpers.add_header2list(
        "Membership Report (prepared {})"
            .format(helpers.date),
        ret, underline_char='=')
    ret.append('Club membership currently stands at {}.'
                  .format(n))
    ret.extend(show.show_applicants_cmd()[:-1])
    # loose the date prepared line       ^^^^^
    try:
        with open(club.ADDENDUM2REPORT_FILE, 'r') as fobj:
            addendum = fobj.read(); addendum=addendum.strip()
            if addendum:
                line = ('Appending addendum as found in file: {}'
                        .format(fobj.name))
                print(line); helpers.add2report(report,line)
                ret.append("")
                ret.append(addendum)
            else:
                line = ("No addendum found in file: {}"
                        .format(fobj.name))
                print(line); helpers.add2report(report,line)
    except FileNotFoundError:
        print('No addendum (file: {}) found.'
                .format(club.ADDENDUM2REPORT_FILE))
    ret.extend(
        ['',
         "Respectfully submitted by...\n\n",
         "Alex Kleider, Membership Chair,",
         "for presentation to the Executive Committee on {}"
         .format(helpers.next_first_friday(exclude=True)),
         "(or at their next meeting, which ever comes first.)",
         ])
    ret.extend(
        ['',
         'PS Zoom ID: 527 109 8273; Password: 999620',
        ])
    print(f"Default file name is '{outfile}'...")
    response = input("Blank to accept or enter new name: ")
    if response:
        outfile = response
    with open(outfile, 'w') as outf:
        outf.write('\n'.join(ret))
    return ret

if __name__ == "__main__":
    report_cmd()

