#!/usr/bin/env python3

"""
A place to prototype new code.
"""

from code import helpers
from code import club
from code import routines
from code import members
from code import show

yearly = club.yearly_dues
n_months = club.n_months
today = helpers.eightdigitdate

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
    
def newbies():
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
    assert len(qres1) == len(qres2)  #{  concistency  }
    assert set1 == set2              #{    checks     }
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


if __name__ == "__main__":
    for line in newbies():
        print(line)
    

#   create_statement(7)
#   ck_distinct_query()
#   show_proration()
#   func2()

