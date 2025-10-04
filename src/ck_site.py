#!/usr/bin/env python3

# File: ck_site.py

"""
Reads the HTML of the Membership page of the Bolinas Rod & Boat
Club's web site and retrieves member (?and applicant?) names.

Next step:
    Collect a similar listing from the data base and compare for
consistency.
"""

import re
import sys
import os
import requests
sys.path.insert(0, os.path.split(sys.path[0])[0])
from code import routines
import glbls

html_file = glbls.html_file
html_file = "/home/alex/Git/Sql/src/m1.html"

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

    m = pat.findall(source)

    if m:
        def f(name):
            return name.split()[1]
        listing = [item[0] for item in m]
        print(f"Found {len(listing)} names in {fname}")
        listing.sort(key=f)
#       print(listing)
        return listing
    else:
        print("No matches found!")


if __name__ == "__main__":
    source = "src/m2.html"
    print(f"html source: {source}")
    listing = html_listing(fname=source)
    if listing:
        with open("names.txt", 'w') as outf:
            for item in listing:
                outf.write(item+"\n")
    else:
        print("No listing!!")

