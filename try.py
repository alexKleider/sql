#!/usr/bin/env python3

"""
A place to prototype new code.
"""

from code import helpers
from code import club
from code import routines
from code import helpers
from code import members

yearly = club.yearly_dues
n_months = club.n_months

def prorate(month, yearly, n_months):
    assert isinstance(month, int)
    assert month > 0
    assert month <= 12
    return round(yearly * n_months[month] / 12)

class RecV1(dict):
    """
    Each instance is a (deep!) copy of rec (a dict)
    and is callable (with a formatting string as a parameter)
    returning the populated formatting string.

    """
    def __init__(self, rec):
#       self = dict(rec)  # this should work but doesn't!!
        for key, value in rec.items():   #} use this method in 
            self[key] = value            #} place of what's above

    def __call__(self, fstr):
        return fstr.format(**self)

def func1():
    l = ["hello", "bye", "so long", ]
    s = set(l)
    print(f"{s}")

def func2():
    d1 = {"husband": "Alex", "wife": "June",
            "daughter": "Tanya", "son": "Kelly", }
#   d2 = dict(d1)
    d2 = helpers.Rec(d1)
    d2["grand_daughter"] = "Isabella"
    print(d1)
    print(d2)
    print(f"it's {d1 is d2} that d1 is d2.")
    print(d2("Wife's name is {wife}."))

def show_proration():
    print("Proration Schedule")
    print(" Mo  Dues")
    print(" ==  ====")
    for month in range(1, 13):
        print(f"{month:>3}: {prorate(month, yearly, n_months)}")

query = f"""SELECT DISTINCT P.personID, P.last, P.first, P.suffix
        FROM People as P    -- if use *, will include all values
        JOIN Person_Status as PS   -- from the Person_Status table
        WHERE P.personID = PS.personID   -- as well!!!
        AND PS.statusID in (11, 15)
        AND (PS.end > "{helpers.eightdigitdate}"
             OR PS.end = "")
        ORDER BY P.last, P.first;"""

f_query = """
SELECT P.personID, P.last, P.first, P.suffix,
        P.email, P.address, P.town, P.state,
        P.postal_code, P.country,
        D.dues_owed, DP.cost, KS.slot_cost, M.owing
        FROM People AS P
        LEFT JOIN Dues AS D ON D.personID = P.personID
        LEFT JOIN Dock_Privileges AS DP ON DP.personID = P.personID
        LEFT JOIN Kayak_Slots AS KS ON KS.personID = P.personID
        LEFT JOIN Moorings AS M ON P.personID = M.personID
        WHERE (D.dues_owed > 0
            or DP.cost > 0 
            or KS.slot_cost > 0 
            or M.owing > 0 )
          AND P.personID ={};"""

def create_statement(personID):
    query = f_query.format(personID)
    keys = ("ID, last, first, suffix, email, "
        + "address, town, state, postal_code, "
        + "country, dues, dock, kayak, mooring")
    listing = routines.query2dict_listing(query,
            keys.split(', '),
            from_file=False)
    if listing:
        person = listing[0]
        total = 0
        for key in ("dues", "dock", "kayak", "mooring"):
            if not person[key]:
                person[key] = 0
            else:
                person[key] = int(person[key])
                total += person[key]
        person['total'] = total
        members.add_statement_entry(person)
        print(f"{repr(person)}")
    else:
        print(f"No result for {personID}.")
#   members.add_statement_entry(data)

def ck_distinct_query():
    listing = routines.fetch(query, from_file=False)
    fname = "temp.txt"
    with open(fname, 'w') as outf:
        for line in listing:
            l = [str(item) for item in line]
            outf.write(', '.join(l)+'\n')
    print(f"Length of listing is {len(listing)}")
    print(f"Sent to {fname}")

if __name__ == "__main__":
    create_statement(7)
#   ck_distinct_query()
#   show_proration()
#   func2()

