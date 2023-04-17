#!/usr/bin/env python3

# File: old2new_dock.py

from code import routines


columns = """
slot_code
personID
slot_cost
"""
keys = columns.split() 

return_line = "19|K-19|100|202"

def entries():
    res = routines.fetch("""
    SELECT * FROM old_Kayak_Slots;
    """, from_file=False)
    listing = []
    for entry in res:
        dic ={}
        dic[keys[0]] = entry[1]
        dic[keys[1]] = entry[-1]
        dic[keys[2]] = entry[-2]
        listing.append(dic)
    return listing

def update_table(listing):
    key_listing = ', '.join(keys)
    query = f"""
    INSERT INTO Kayak_Slots 
    ({key_listing})
    VALUES
    {{}};
    """
    for entry in listing:
        values = tuple([value for value in entry.values()])
        q = query.format(repr(values))
#       print(q)
#       _ = input(f"query: {q}")
        routines.fetch(q, from_file=False, commit=True)


if __name__ == "__main__":
    update_table(entries())

