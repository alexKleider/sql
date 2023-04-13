#!/usr/bin/env python3

# File: old2new_applicants.py

from code import routines
from code import alchemy


def get_sponsorID(name):
    ret = routines.fetch("""
        SELECT personID, first, last FROM People
        WHERE first = ? AND last = ?;
        """, from_file=False,
            params=(name.split()))
    return ret[0][0]


def main0():
    res = alchemy.alch("""
            SELECT * FROM oldApplicants;
            """, from_file=False)
    for line in res:
#       _ = input(f"line: {line}")
        new_dict = {}
    for key in line.keys():
        new_dict[key] = res[key]
#   _ = input(f"new_dict: {new_dict}")
    spID =  get_sponsorID(line['sponsor1'])
#   _ = input(f"spID: {spID}")

    new_dict['sponsor1'] = spID
    new_dict['sponsor2'] = get_sponsorID(line['sponsor2'])

def entries():
    columns1 = """
    personID sponsor1 sponsor2 app_rcvd
    fee_rcvd meeting1 meeting2 meeting3 approved
    inducted dues_paid
    """
    columns2 = """
    personID sponsor1ID sponsor2ID app_rcvd
    fee_rcvd meeting1 meeting2 meeting3 approved
    dues_paid notified
    """
    keys1 = columns1.split() #keys of oldApplicants
    keys2 = columns2.split() #keys of newApplicants
    res = routines.fetch("""
            SELECT * FROM oldApplicants;
            """, from_file=False)
#   _ = input(f"res: {res}")
    listing = []  # for newApplicants
    for entry in res:
        line = entry[1:]  # ignore 1*key and last two
        dict1 = {key: value for key, value in zip(keys1, line)}
        dic = {}
        dic['personID'] = dict1['personID']
        dic["sponsor1ID"] = get_sponsorID(dict1['sponsor1'])
        dic["sponsor2ID"] = get_sponsorID(dict1['sponsor2'])
        for n in range(3, 9):
            dic[keys2[n]] = dict1[keys1[n]]
#       _ = input(f"dic: {dic}\ndict1: {dict1}")
        dic["dues_paid"] = dict1["dues_paid"]
        dic["notified"] = dict1["inducted"]
#       print(dic)
        listing.append(dic)
    return listing

def update_table(listing):
    keys = listing[0].keys()
    key_listing = ', '.join(keys)
    part2 = ', '.join([f':{key}' for key in keys])
    query = f"""
    INSERT INTO Applicants 
    ({key_listing})
    VALUES
    {{}};
    """
    for entry in listing:
        values = tuple([value for value in entry.values()])
        q = query.format(repr(values))
        print(q)
#       _ = input(f"query: {q}")
        routines.fetch(q, from_file=False, commit=True)


if __name__ == "__main__":
    update_table(entries())

