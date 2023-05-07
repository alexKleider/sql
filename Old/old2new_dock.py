#!/usr/bin/env python3

# File: old2new_dock.py

from code import routines

print("So far so good.")

columns = """
personID
cost
"""
keys = columns.split() 

def entries():
    res = routines.fetch("""
    SELECT * FROM old_Dock_Privileges;
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
    INSERT INTO Dock_Privileges 
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

