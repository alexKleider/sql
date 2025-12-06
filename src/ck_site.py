#!/usr/bin/env python3

# File: ck_site.py

"""
Code to check consistency of what's published on the membership
page of the web site vs what's in the Club database.

Reads the HTML of the Membership page of the Bolinas Rod & Boat
Club's web site and retrieves member (?and applicant?) names.

Expect to find the web site data (membership page) @
html_file == "~/www/members.html"
For testing purposes: 
/home/alex/Git/Sql/src/memb.html
"""

import re
import sys
import os
import requests
sys.path.insert(0, os.path.split(sys.path[0])[0])
from code import routines
from code import helpers

html_file = "/home/alex/Git/Sql/src/memb.html"
html_file = "/home/alex/www/members.html"
eightdigitdate = helpers.eightdigitdate

def f(name):
    """returns the second item in an iterable <name)"""
    return name.split()[1]

def html_listing(fname=None):
    f"""
    Returns a sorted listing of the names provided in the
    HTML file found specified (defaults to {html_file}.)
    """
    if not fname:
        fname = html_file
    print("Getting info from ...")
    print(f"  {fname}")
    short_fname = fname.split('/')[-1]

    with open(fname, 'r') as inf:
        source = inf.read()
    #for c in "*@^%":
    #    source = source.replace(c, '')
    #with open("source.txt", 'w') as outf:
    #    outf.write(source)

    pat = re.compile(r"""</span><span>[@^*%]?
    ([A-Z][a-zA-Z]*\ [A-Z][a-zA-Z]*(\ [A-Z][a-zA-Z]*)?)
    </span><span>&lt;/<span\ class="end-tag">strong</span>&gt;
    </span><span></span><span>&lt;<span\ class="start-tag">br</span>&gt;
    </span><span>\ Phone: """, re.VERBOSE)
    pat = re.compile(r"""
<p\ class=""\ style="white-space:pre-wrap;"><strong>[@^*%]?
([A-Z][a-zA-Z]*\ [A-Z][a-zA-Z]*(\ [A-Z][a-zA-Z]*)?)
</strong><br>\ Phone:
    """, re.VERBOSE)
    # modify to account for possibility of...
    # *, ^, @, % as a prefix   and
    # _, (, ), ' within a name.
    pat = re.compile(r"""
<p\ class=""\ style="white-space:pre-wrap;"><strong>
(?P<prefix>[@^*%]?)
(?P<name>([A-Z][_()'éa-zA-Z]*\ [A-Z][a-zA-Z]*(\ [A-Z][-_()'a-zA-Z]*)?))
\ ?</strong><br>\ Phone:""", re.VERBOSE)

    m = pat.finditer(source)

    if m:
        listing = [item["name"] for item in m]
        print(f"Found {len(listing)} names in {fname}")
#       _ = input(listing)
        listing.sort(key=f)
#       print(listing)
        return listing
    else:
        print("No matches found!")


def getfromdb():
    """
    retrieve a listing of member (& applicant) names
    """
    query = f"""
/* Sql/web_listing.sql */
-- !! Requires formatting: eightdigitdate x2!!
/* collect all who should be listed on the web site  */
SELECT
--  P.personID, P.first, P.last, P.suffix, P.email, P.address,
--  P.town, P.state, P.postal_code, P.phone
    P.first, P.last, P.suffix
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE
(PS.statusID in (1,2,3,4,5,6,7,8,9,10,  -- applicants
                11, 15,  -- 1st yr and "in good standing"
                14, 16,  -- honourary, inactive
                17, 19)) -- retiring, fees waived

AND (PS.begin = '' OR PS.begin <= '{eightdigitdate}')
AND (PS.end = '' OR PS.end > '{eightdigitdate}')
ORDER BY
    P.last, P.first, P.suffix
; """
#   print(query)
    res = routines.fetch(query, from_file=False)
    ret = []
    for item in res:
#       print(item)
        s = ' '.join(item[:-1])
        if item[-1]: s = s + item[-1]
        ret.append(s)
    return ret




db_results = "db_names.txt"
html_results = "html_names.txt"

def send2files():
    from_db = getfromdb()
    if from_db:
        with open(db_results, 'w') as outf:
            for item in from_db:
                outf.write(item+"\n")
        print(f"{db_results} written")
    else:
        print("No Club db results!!")
        
    source = "/home/alex/Git/Sql/src/m0.html"
    print(f"html source: {source}")
    listing = html_listing(fname=source)
    if listing:
        with open(html_results, 'w') as outf:
            for item in listing:
                outf.write(item+"\n")
        print(f"{html_results} written")
    else:
        print(f"No html results!!")

if __name__ == "__main__":
    from_db = set(getfromdb())
    from_html = set(html_listing(fname=html_file))
    db_only = from_db - from_html
    html_only = from_html - from_db
    db_listing = list(db_only)
    html_listing = list(html_only)
    res = ["In database only:",]
    db_listing.sort(key=f)
    for item in db_listing:
        res.append(item)
    res.extend(['',"In html only:",])
    html_listing.sort(key=f)
    for item in html_listing:
        res.append(item)
    for item in res:
        print(item)
