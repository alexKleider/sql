#!/usr/bin/env python3

# File: old2new_dues.py

from code import routines

print("So far so good.")

columns = """
personID
dues_owed
"""
keys = columns.split() 

def entries():
    res = routines.fetch("""
    SELECT * FROM old_Dues;
    """, from_file=False)
    listing = []
    for entry in res:
        dic = {key: value for key, value in zip(
            columns.split(), entry)}
        listing.append(dic)
    return listing

def update_table(listing):
    key_listing = ', '.join(keys)
    query = f"""
    INSERT INTO Dues 
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

