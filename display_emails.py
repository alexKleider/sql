#!/usr/bin/env python3

# File: display_emails.py

"""
Usage:
    $ ./display_emails.py [outfile]

If not specified, <outfile> defaults to "emails.txt".
"""

import sys
from code import club
from code import helpers

default_in_file = 'Secret/emails.json'
default_out_file = 'emails.txt'

if len(sys.argv) > 1:
    outf = sys.argv[1]
else:
    outf = default_out_file

print(f"Using {default_in_file} as default  input file...")
inf = input(f"<Enter> to accept or enter an alternative: ")
if inf: default_in_file = inf


def display_emails_cmd(infile=club.Holder.email_json):
    records = helpers.get_json(infile, report=True)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
#           _ = input("{}: {}".format(field, record[field]))
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)

if __name__ == '__main__':
    with open(outf, 'w') as stream:
        print(f"Opening file '{stream.name}'...")
        stream.write(display_emails_cmd())
    print(f"Ouput written to {outf}")

