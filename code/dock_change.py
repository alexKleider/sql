#!/usr/bin/env python3

# File: code/dock_change.py 

import club
import routines

"""
initiate_dock is useless to me!
The default value is already populated in the data base.
Work on this if/when fee changes
or need to add or remove someone.
i.e. have:
    add_dock_user
    rm_dock_user
    change_default_cost    }
    universal_add_dock_fee }
    The last two would be essentially the same!
"""

query = """
    INSERT INTO Dock_Privileges
    (personID)
    VALUES (?);
"""


def initiate_dock():
    with open(club.dock_file, 'r') as inf:
        for line in inf:
            line = line.strip()
            if not line or line.startswith('#'): continue
            name, fee = line.split(':')
            first, last = name.split()
            fee = int(fee)
            ID = routines.get_ids_by_name(first, last)
            if len(ID) > 1:
                print("Not equiped to handle more than one ID")
                _ = input("Suggest aborting (^C).")
            ID = ID[0][0]
            print(
        f"{ID:>3}: {first.strip()} {last.strip()}: {fee}")
            res = routines.get_query_result(query,
#                       db=db_file_name,
                        params=(ID,),
#                       data=None,
                        from_file=False, 
                        commit=True)
            print(res)

if __name__ == '__main__':
    pass

