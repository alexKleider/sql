#!/usr/bin/env python3

# File: code/listings.py

"""
As of Fri 23 Aug 2024 10:59:51 AM PDT
Developed sponsors.py (which creates a csv of applicants
with the names of their sponsors. This seems the logical
place for that code to live.

Old thinking...
As of Fri 19 Apr 2024 05:45:28 PM PDT
There's nothing of importance here.
Keeping this file as a possible location for code
that provides data listings.
Currently such code is spread out all over the code base.
This might be a place to separate the presentation from 
the code that gathers the data.
Current content should probably be incorporated into ck_data
or not except perhaps to check that membership doesn't exceed
200.
"""

try: from code import helpers
except ImportError: import helpers
try: from code import routines
except ImportError: import routines

m0_file = "first_yr_members.txt"
m1_file = "members_in_good_standing.txt"


date = helpers.eightdigitdate

query = routines.import_query("Sql/members1stYr_f.sql")
query = query.format(date, date)
#print(query)
retm0 = routines.fetch(query, from_file=False)

query = routines.import_query("Sql/members_igs_f.sql")
query = query.format(date, date)
#print(query)
retm1 = routines.fetch(query, from_file=False)

def how2sort(item):
    if item[3]:
        last = item[2] + item[3]
    else:
        last = item[2]
    return(f"{last}, {item[1]}")


def sponsors(report=None):

    def id2name(_id):
        res = routines.fetch(f_query.format(_id), from_file=False) 
        first, last = res[0]
        return f"{first} {last}"


    out_f_name = "sponsors.csv"

    query1 = """
    SELECT P.personID, P.first, P.last, A.sponsor1ID, A.sponsor2ID
                            FROM People AS P
    JOIN Applicants as A
    WHERE P.personID = A.personID
    ;"""

    f_query = """
    SELECT first, last from People where personID = {}
    ;"""

    applicant_generator = routines.dicts_from_query(query1,
        keys = "ID, first, last, s1, s2".split(', '))
    applicants = [applicant for applicant in applicant_generator]
    for d in applicants:
        d["s1"] = id2name(d["s1"])
        d["s2"] = id2name(d["s2"])
    helpers.dump2csv_file(applicants, file_name = out_f_name)
    print(f"Results dumped to {out_f_name}")

if __name__ == "__main__":
    print(
        f"Number of first year members:           {len(retm0)}")
    print(
        f"Number of 'members in good standing': {len(retm1)}")
    all = sorted((retm0 + retm1), key=how2sort)
    print(
        f"For a total of {len(all)}")
    with open(m0_file, 'w') as outf:
        outf.write('\n'.join([how2sort(item) for item in retm0]))

    with open(m1_file, 'w') as outf:
        outf.write('\n'.join([how2sort(item) for item in retm1]))
    print(
        f"Listings sent to {m0_file} and {m1_file}.")

    


