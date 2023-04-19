#!/usr/bin/env python3

# File: code/multiple.py

"""
A place to put routines supporting what began as
my code to support entry of dated events: date.py
"""

try: from code import routines
except ImportError: import routines

def update_dues(data):
    """
    subtract data['dues'] from data['personID']'s dues_owed.
    """
    _ = input(
    f"""Running code.multiple.update_dues:
    The following dict must contain personID and dues:
        data: {data}""")
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
    """
    For now we'll assume no one ever pays a fee for which there
    isn't an entry in their name.
    """
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


def send_acknowledgement(data):
    """
    <holder> must be able to format ${payment} and
    {extra} (a statement of what's being acknowledged.)
    """
    holder = club.Holder()
    holder.data = data
    holder.which = content.content_types["thank"]
    ret = []
    # give user opportunity to abort if files are still present:
    helpers.check_before_deletion((holder.email_json,
                                    holder.mail_dir),
                                    delete=True)
    os.mkdir(holder.mail_dir)
    ret.extend(commands.assign_templates(holder))
    holder.emails = []
    # no need for "holder_funcs": we've already got our data
    members.thank_func()
    pass
    # send holder.emails to a json file
    helpers.dump2json_file(holder.emails, holder.email_json)
    # Delete mailing dir if no letters are filed:
    if os.path.isdir(holder.mail_dir) and not len(
            os.listdir(holder.mail_dir)):
        os.rmdir(holder.mail_dir)
        print("Empty mailing directory deleted.")
    else:
        print("""..next step might be the following:
    $ zip -r 4Peter {0:}
    (... or using tar:
    $ tar -vczf 4Peter.tar.gz {0:}"""
            .format(holder.mail_dir))
    print("send_acknowledgement completed..")
    return ret

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

