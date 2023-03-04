#!/usr/bin/env python3

# File: code/initiate_dues.py

"""
No need for this now that Dues table has been populated.
"""

def add_dues_cmd():
    """
    UPDATE Dues SET dues_owed = dues_owed + 100
    -- WHERE id = 1;
    Currently Dues table is empty.
    Need to make an entry for each member.
    """
    # first get a list of personID(s)
    query = """
    SELECT People.personID, first, last
    FROM People, Person_Status, Stati
    WHERE
        Person_Status.personID = People.personID
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = 'm'
    ;
    """
    res = routines.get_query_result(
            query, from_file=False, commit=False)

    # Now add dues for each personID:
    query = """INSERT INTO Dues (personID, dues_owed)
                VALUES (?, ? );
            """
    con = sqlite3.connect(club.db_file_name)
    cur = con.cursor()
    ret = []
    for entry in res:
        cur.execute(query, (entry[0], club.yearly_dues, ))
        ret.append('Added {} on behalf of {} {}'
            .format(club.yearly_dues, entry[1], entry[2]))
    con.commit()
    return ret

