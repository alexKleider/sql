#!/usr/bin/env python3

# File: code/multiple.py

"""
A place to put routines supporting what began as
my code to support entry of dated events: date.py
"""

try: from code import routines
except ImportError: import routines

def update_account(query):
    ret = (["Query is ...", query])
    ret.append("Query returns:")
    ret.append(repr(routines.fetch(query,
            from_file=False, commit=True)))
    return ret

def update_dues(data):
    """
    subtract data['dues'] from data['personID']'s dues_owed.
    """
#   _ = input(
#   f"""Running code.multiple.update_dues:
#   The following dict must contain personID and dues:
#       data: {data}""")
    ret = ["Updating dues...", ]
    query = """UPDATE Dues SET
        dues_owed = dues_owed - {dues}
        WHERE personID = {personID};
        """.format(**data)
    ret.extend(update_account(query))
    return ret

def update_dock(data):
    ret = ["Updating dock...", ]
    query = """UPDATE Dock_Privileges SET
        cost = cost - {dock}
        WHERE personID = {personID};
    """.format(**data)
    ret.extend(update_account(query))
    return ret

def update_kayak(data):
    ret = ["Updating kayak...", ]
    query = """UPDATE Kayak_Slots SET
        slot_cost = slot_cost - {kayak}
        WHERE personID = {personID};
    """.format(**data)
    ret.extend(update_account(query))
    return ret

def update_mooring(data):
    ret = ["Updating mooring...", ]
    query = """UPDATE Moorings SET
        owing = owing - {mooring}
        WHERE personID = {personID};
    """.format(**data)
    ret.extend(update_account(query))
    return ret

def credit_accounts(data):
    """
    For now we'll assume no one ever pays a fee for which there
    isn't an entry in their name.
    """
    names = routines.get_person_fields_by_ID(
            data['personID'],
            fields=('first', 'last', 'suffix'))
    data["name"] = "{} {} {}".format(*names).strip()
    ret = [f'Crediting accounts for {data["name"]}', ]
    keys = data.keys()
    if 'dues' in keys:
        ret.extend(update_dues(data))
    if 'dock' in keys:
        ret.extend(update_dock(data))
    if 'kayak' in keys:
        ret.extend(update_kayak(data))
    if 'mooring' in keys:
        ret.extend(update_mooring(data))
    return ret


def ret_0statement_dict():
    """
    Returns a dict keyed by personID.
    Each value is a dict keyed by account (dues, dock, etc)
    with amount owed as values (including where value is 0)
    """
    byID = dict()  # to be assigned to holder.working_data
    source_files = {
            # the following files all check for membership.
            # hence the 'f' for formatted by helpers.sixdigitdate
            # the "0" indicates that zero balances are included
            'dues': "Sql/dues0_f.sql",
            'dock': "Sql/dock0_f.sql",
            'kayak': "Sql/kayak0_f.sql",
            'mooring': "Sql/mooring0_f.sql",
            }
    for key in source_files.keys():
        query = routines.import_query(source_files[key]
                            ).format(helpers.sixdigitdate)
        res = routines.fetch(query, from_file=False)
        if res:
            for entry in res:
                _ = byID.setdefault(entry[0], {})
                byID[entry[0]][key] = entry[1]
    return byID



def one_time_test():
    data = dict(
            personID= 119,
            date_received= '20230407',
            dues= 50,
            acknowledged= '20230410',
            )
    for line in credit_accounts(data):
        print(line)

if __name__ == '__main__':
    print("Dry run of code/multiple.py")
#   one_time_test()
    pass

