#!/usr/bin/env python3

# File: old2new_applicants.py

from code import routines
from code import alchemy


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
    columns = """
    personID sponsor1ID sponsor2ID app_rcvd
    fee_rcvd meeting1 meeting2 meeting3 approved
    dues_paid notified
    """
    keys = columns.split() #keys of Applicants
    res = routines.fetch("""
            SELECT * FROM old_Applicants;
            """, from_file=False)
#   _ = input(f"res: {res}")
    listing = []  # for newApplicants
    for entry in res:
        line = entry[1:]  # ignore 1*key
        dic = {key: value for key, value in zip(keys, line)}
#       print(dic)
        listing.append(dic)
    return listing

def update_table(listing):
    keys = listing[0].keys()
    key_listing = ', '.join(keys)
#   part2 = ', '.join([f':{key}' for key in keys])
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

