#!/usr/bin/env python3

# File: code/multiple.py

try: from code import routines
except ImportError: import routines

def update_dues(data):
#   _ = input(f"data: {data}")
    ret = ["Updating dues...", ]
    query = """UPDATE Dues SET
        dues_owed = dues_owed - {dues}
        WHERE personID = {personID};
        """.format(**data)
    ret.extend(["Query is ...", query])
    ret.append("Query returns:")
    ret.append(routines.fetch(query,
            from_file=False, commit=True))
    return ret

def update_dock(data):
    ret = ["Updating dock...", ]
    return ret

def update_kayak(data):
    ret = ["Updating kayak...", ]
    return ret

def update_mooring(data):
    ret = ["Updating mooring...", ]
    return ret

def credit_accounts(data):
    names = routines.get_person_fields_by_ID(
            data['personID'],
            fields=('first', 'last', 'suffix'))
    data["name"] = "{} {} {}".format(*names).strip()
    ret = [f'Crediting accounts for {data}', ]
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


def send_letter(data):
    pass

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
#   one_time_test()
    print("Dry run of code/multiple.py")
    pass

