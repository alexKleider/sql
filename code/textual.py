#!/usr/bin/env python3

# File: code/textual.py

""" Gui-like interface:
Using pysimplegui @
https://www.pysimplegui.org/en/latest/#github-statistics
(See also https://textual.textualize.io/getting_started/
as a possible alternative.)

Might consider using a context manager as at
https://iamshobhitagarwal.medium.com/context-manager-in-python-df486d8cfed2
class CustomContext:
    def __enter__(self):
        # Setup code
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        pass
        # Teardown code

    with CustomContext() as custom:
        # Code inside this block
    # Teardown code is automatically executed

TO DO:
    <change_mapping> and <change_or_add_values> are essentially
    the same thing with the exception that the latter includes
    reporting. Rename latter to former.
"""

try:
    import routines
    import helpers
except ImportError:
    from code import routines
    from code import helpers
import PySimpleGUI as sg
font_index = 1  # adjust for readability
fonts = (          #  vv -- size parameter
        ("Helvetica", 10),  # the default
        ("Helvetica", 15),
        ("Helvetica", 20),
        ("Helvetica", 25),
        )
font= fonts[font_index]
    # Above code only to adjust size for readability
    #making text large enough to read.  Default size is 10.

def yes_no(text, title="Run query?"):
    return sg.popup_yes_no(text,
            title=title, font=font) == "Yes"


def valid_values(ev, allow_blanks=False):
    """
    <ev> is what's returned by sg's window.read()
    Returns a dict if values are valid, 
    Returns a string if not.
    Only one client in this module: <get_fields4> which
    is planned for deprication in favour of <get_fields>.
    """
    event, the_dict = ev
    if event in (None, "Cancel"):
        return "None or Cancel"
    if not allow_blanks:
        if '' in the_dict.values():
            return "Missing value(s)"
    return the_dict

def show_fonts():
    couriers = ["BPG Courier", "GPL&GNU",
                "BPG Courier", "S GPL&GNU",
                "Courier 10 Pitch",
                "Free Courier",
                ]
    fonts = sg.Text.fonts_installed_list ()
    for font in fonts:
        if "Courier" in font:
            print(font)
    

def f2run():
    _ = input("Running function f2run")

    
def a_show_stati(f2run, font=font):
    """
    A work in progress
    """
    keys = routines.keys_from_schema("Stati")
    res = routines.fetch("SELECT * FROM Stati;",
            from_file=False)
    layout = [[sg.Text("Stati table fields:",)],]
    layout.extend([
#       [sg.Text(repr(item), pad=(0,(0,0))),]
        [sg.Text("{0:>2}: {1:>4},  {2:}".format(*item),
                    pad=(1,(0,1)), font=("Free Courier", 7))]
        for item in res
        ])
    window = sg.Window("For Info", layout,
                       font=font, finalize=True)
    f2run()
    ret = window.read()

def show_stati(font=font):
    """
    Provides an info box showing the stati:
    ...stays open until explicitly closed.
    """
    keys = routines.keys_from_schema("Stati")
    res = routines.fetch("SELECT * FROM Stati;",
            from_file=False)
    layout = [[sg.Text("Stati table fields:",)],]
    layout.extend([
#       [sg.Text(repr(item), pad=(0,(0,0))),]
        [sg.Text("{0:>2}: {1:>4},  {2:}".format(*item),
                    pad=(1,(0,1)), font=("Free Courier", 7))]
        for item in res
        ])
    window = sg.Window("For Info", layout, font=font)
    ret = window.read()


def get_fields(fields, header="Enter values for each key",
               font=font):
    """
    Prompts user to supply values for each field.
    Returns None if user aborts, otherwise...
    Returns a dict keyed by <fields>,
    values are the entered (possibly empty) strings
    # Has been tested.
    # Best to use <change_mapping> instead?
    """
    layout = [[sg.Text(header)],]
    layout.extend([
        [sg.Text(field), 
            sg.Input(expand_x=True, key=field)]
        for field in fields
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window('Enter values', layout, font=font)
#   event, values = window.read()
    event, the_dict = window.read()
    window.close()
    if event in (None, "Cancel"):
        return
    return the_dict
# end of get_fields

def change_mapping(mapping,
            headers=["Correct or Enter new value(s)",
                    "Choose from...",], font=font):
    """
    Prompts user to change/enter mapping values.
    Returns a new/modified dict or None if user aborts.
    <mapping> remains unchanged.
    """
    layout = [[sg.Text(headers[0])],]
    layout.extend([
        [sg.Text(key), 
            sg.Input(expand_x=True, key=key, default_text=value)]
        for key, value in mapping.items()
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window(headers[1], layout, font=font)
    event, new_dict = window.read()
    window.close()
    if event in (None, "Cancel"):
        return
    return new_dict

def change_or_add_values(mapping, report=None,
            headers=["Correct or Enter new value(s)",
                    "Choose from...",], font=font):
    """
    Prompts user to change/add mapping values.
    Returns the modified dict or None if user aborts.
    Exactly the same code as <change_mapping> with addition of
    <report>ing functionality.
    """
    helpers.add2report(report,
        "Entering code/textual.change_or_add_values...")
    layout = [[sg.Text(headers[0])],]
    layout.extend([
        [sg.Text(key), 
            sg.Input(expand_x=True, key=key, default_text=value)]
        for key, value in mapping.items()
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window(headers[1], layout, font=font)
#   event, values = window.read()
    event, new_dict = window.read()
    window.close()
    if event in (None, "Cancel"):
        helpers.add2report(report,
            "...change_or_add_values cancelled.")
        return
    helpers.add2report(report,
        "...change_or_add_values returning a new dict.")
    return new_dict

def test_cora():
    mapping=dict(first= "Alex",
                last="Kleider",
                date1 ="",
                )
    ret = change_or_add_values(mapping)
    if ret == None: print("Returned None")
    else:
        for key, value in ret.items():
            print(f"{key}: {value}")

    

def get_fields4(p_data, fields):
    """
    Will probably deprecate in favour of get_fields()
    Prompts user to supply values for each field.
    <p_data>, a dict, informs for which person data is being
    collected and must at minimum include first, last & suffix.
    Returned are the values (if provided), else None
    """
    header = (
        "Enter data for {personID}: {first} {last} {suffix}"
                            .format(**p_data))
    layout = [[sg.Text(header)],]
    layout.extend([
        [sg.Text(field), 
            sg.Input(expand_x=True, key=field)]
        for field in fields
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window('Enter values', layout, font=font)
#   event, values = window.read()
    ret = window.read()
    window.close()
    ret = valid_values(ret)
    return ret


def get_stati(personID):
    """
    ## Was called get_mode(
    collects Person_Status table entries for person IDed.
    """
    ps_fields = routines.keys_from_schema("Person_Status")
    res = routines.fetch(f"""SELECT * FROM Person_Status
            WHERE personID = {personID}; """, from_file=False)
#   _ = input(repr(res))  #!# <res> is NOT USED!!!

def edit_person_status(
#def get_mode(
        person_data, fields,
        fstring="Member: {personID:>3} {first} {last} {suffix}"):
    """
    # Under development: totally inappropriate name changed!
    <person_data> is a dict.
    User given opportunity to select fields and whether to
    INSERT a new record or UPDATE an existing one.
    Returns a query string or None.
    """
    layout = [
        [sg.Text(fstring.format(**person_data))],
        [sg.Radio("INSERT", "RADIO", key='-INSERT-'),
        sg.Radio("UPDATE", "RADIO", key='-UPDATE-')],
        [sg.Text('Choose Fields',justification='left')],
        [sg.Listbox(values=[field for field in fields],
            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            key='-FIELDS-', size=(30,6))],
        [sg.Button('SAVE',), sg.Button('CANCEL',)],
            ]
    win = sg.Window('Action desired', layout)
    e, v = win.read()
    fields2add = v['-FIELDS-']
    win.close()
    if e != 'SAVE':
        print(f"Decided to {e}")
        return
    else:
        mapping = get_fields(fields2add)
        if not mapping:
            print("Aborting code.textual.get_mode")
            return
    keys = ', '.join(mapping.keys())
    values = ', '.join(mapping.values())
    if v['-INSERT-']:
        keys = 'personID, ' + keys
        values = f'{person_data["personID"]}, ' + values
        # easy: just create query for a new entry...
        query = f"""INSERT INTO Person_Status ({keys})
                    VALUES ({values})
                    ; """
        return query
    elif v['-UPDATE-']:
        # Must 1st find out which entry to update...
        query = f"""SELECT * FROM Person_Status
        WHERE personID = {person_data[personID]};"""
        return query
        kv = zip(keys,values)
        listofstrings = [f"{key} = {value}" for 
                key, value in kv]
        entries = ', '.join(listofstrings) 
        old_values = 'old values'
        query = f"""UPDATE Person_Status SET
        {entries}
        WHERE {old_values}
        ;"""
        fields2update = v['-FIELDS-']
        print(f"fields2update: {repr(fields2update)}")
        return query
    else:
        assert False, "Impossible option in textual.get_mode"


note = """
'SAVE' {'-INSERT-': False, '-UPDATE-': True, '-FIELDS-': ['begin', 'end']}
"""

def get_demographics(applicant=True, report=None, font=font):
    """
    Uses a GUI to collect all demographic data needed to create
    an entry into the People table AND (unless <applicant> is set
    to <False>) also collect entries for two sponsor names and
    app_rcvd and fee_rcvd fields.
    Caution: do not hit the minimize button ([_] top right
    corner!) This causes the system to hang!!!
    Returns a dict or None (if user aborts.)
    Client is code/data_entry.py
    """
    helpers.add2report(report,
            "Entering code/textual/get_demographics...")
    fields = routines.keys_from_schema("People", brackets=(1,0))
    if applicant==True:
        fields.extend(["sponsor1", "sponsor2", "app_rcvd", "fee_rcvd"])
    layout = [  # the entry fields...
            [sg.Text(f_name),
                sg.Input(expand_x=True, key=f_name)]
            for f_name in fields
            ]    #  ...now and two Buttons:
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window('Enter demographics', layout, font=font
#               no_titlebar=True
                )
    event, values = window.read()
    window.close()
    if event in (None, 'Cancel'):
        helpers.add2report(report,
                "... gui/get_demographics returning None.")
        return
    elif event == 'OK':
        data = values
        entry = ["... gui/get_demographics returning:"]
        for key, value in data.items():
            entry.append(f"\t{key}: {value}")
        helpers.add2report(report, entry)
        return data
    else:
        assert False, f"!Unexpected event: {repr(event)}!"


def create_dem_file(data, report=None):
    """
    Creates a "flDem.txt" file.
    Uses data collected by get_demographics()
    to create a text file showing the data collected.
    Differs from a Secret/flAp.txt file in that
    sponsor data is missing.
    """
    record = helpers.Rec(data)
    for key, value in record.items():
        print(f"key: {key},  value: {value}")
    fname = ('Secret/Applicants/' +
            record['first'][0].lower() +
            record['last'][0].lower() +
            record['suffix'] +
            'Dem.txt')  # No sponsor data included!!
    if not record['suffix']:
        record['suffix'] = 'No Suffix'
    with open(fname, 'w') as outf:
        outf.write(f"# File: {fname}\n")
        outf.write(
          f"# {record['first']} {record['last']} " +
          f"{record['suffix']} {helpers.date}\n")
        outf.write("\n")
        for key, value in record.items():
            if key == 'suffix':
                if not value:
                    outf.write("No Suffix\n")
                else:
                    outf.write(value+'\n')
            else:
                outf.write(value+'\n')

def people_choices(header_prompt=None, report=None,
                   font=font):
    """
    GUI method of getting a list of people records.
    Returns a listing of dicts keyed by ID, first, last
    OR None (if user cancels/quits, no entries are made
    or no results obtained.)
    Use '%' wild card for selection.
    1st step in providing 
    code/routines/pick_People_record functionality!
    """
    helpers.add2report(report,
            "Entering code/textual/people_choices...")
    keys = routines.keys_from_schema("People")
    fields = keys[1:4]
    layout = [[sg.Text(f_name), sg.InputText()]
                    for f_name in fields  ]
    layout.append([sg.Button('OK'),
                        sg.Button('Cancel')])
    window = sg.Window(
        'Enter hints using "%" as wild cards:',
                                    layout, font=font)
    data = None
    event, values = window.read()
    if event == 'OK':
        if set(values.values()) == {''}:
            # all empty strings i.e. no data entered
            report.append(
                "textual/people_choices got an empty list; " +
                "returning None")
            return
        data = {}
        for n in range(len(values)):
            data[fields[n]] = values[n]
    elif event in (None, "Cancel"): 
        report.append(
            "textual/people_choices aborted; returning None")
        return
    else:
        assert False, f"Unexpected event: {repr(event)}"
    window.close()
    # report prn (expect to redact this section...
    helpers.add2report(report, "First window returning:")
    for key, value in data.items():
        helpers.add2report(report,
                f"key: {key}   value: {value}")
    # use hints to get candidates:
    query_lines = [
        "SELECT *",
            "FROM People WHERE ", ]
    additional_lines = []
    if data['first']:
        additional_lines.append(
            f"""first LIKE "{data['first']}" """)
    if data['last']:
        additional_lines.append(
            f"""last LIKE "{data['last']}" """)
    if data['suffix']:
        additional_lines.append(
            f"""suffix LIKE "{data['suffix']}" """)
    additional_lines = " AND ".join(additional_lines)
    query_lines.append(additional_lines)
    query = ' '.join(query_lines)
    query = query+"ORDER BY last, first"+';'
#   _ = input(f"query is {repr(query)}")
#   ret = routines.fetch(query, from_file=False)
    ret = routines.query2dict_listing(query, keys,
            from_file=False)
#   _ = input(f"{repr(ret)}")
    helpers.add2report(report, "query returning:")
    for item in ret:
        helpers.add2report(report, repr(item))
    helpers.add2report(report,
        "...leaving code/textual.people_choices()")
    return ret


def test_people_choices():
    report = []
    res = people_choices(report=report,
        header_prompt = "Choose from the People table...")
    if not res:
        print(f"people_choices returned {repr(res)}")
    else:
        print("pick_People_record returning the following...")
        for item in res:
            print("{personID:>3} {first} {last}".format(
                **item))
#   print("\nReport follows...")
#   print('\n'.join(report))


def pick(query, format_string,
                header="CHOOSE ONE",
                subheader="Choices are...",
                report=None):
    """
    Uses <query> to collect a list of dicts and presents
    user with a list of choices dictated by
    the format_string.
    Returns chosen dict or None (if none available or
    user aborts/cancels.)
    """
    helpers.add2report(report,
        "Entering code.textual.pick", also_print=False)
    mappings = routines.query2dicts(query)
    if not mappings:
        helpers.add2report(report,
                "No records provided ==> exit",
                also_print=True)
        return
    options = [format_string.format(**rec)
            for rec in mappings]
    listing = zip(range(len(options)), options)
    for_display = [f"{item[0]:>2}: {item[1]}"
                for item in listing]
    layout=[[sg.Text(subheader,size=(50,1),
#           font='Lucida',justification='left'
            )],
            [sg.Listbox(values=for_display,
                select_mode='extended',
                key='CHOICE', size=(50,len(mappings)))],
            [sg.Button('SELECT',
#               font=('Times New Roman',12)
                ),
            sg.Button('CANCEL',
#                   font=('Times New Roman',12)
                    )
            ]]
    win =sg.Window(header,layout)
    e, v = win.read()
    win.close()
    if not v["CHOICE"]:
        return
    chosen_item = v['CHOICE'][0].strip().split()[0][:-1]
    if (e != "SELECT") or not v['CHOICE']:
        helpers.add2report(report,
            "pick returning None", also_print=True)
        return
    else:
        helpers.add2report(report,
            ["code.textual.pick:",
            "  line chosen...",
            f"    {repr(v['CHOICE'])}",
            "  record returned:",
            f"    {repr(mappings[int(chosen_item)])}"],
            also_print=False)
        return mappings[int(chosen_item)]


def choose(records, header="CHOOSE ONE",
                    subheader="Pick a person",
                    report= None):
    """
    <records> are a list of dicts each representing an
    entry from the People table. Fields personID, first
    and last are presented for consideration.
    Returns one of the dicts
    or something that'll evaluate to False
    Adds to <report> (a list of strings) if provided.
    Used by <selectP_record> but should probably be redacted
    in favour of <pick> and <selectP_record> should be
    adjusted accordingly.
    """
    #set the theme for the screen/window
    helpers.add2report(report,
            "Entering code.textual.choose")
    if not records:
        helpers.add2report(report,
                "No records provided ==> exit")
        return
#   sg.theme('SandyBeach')
    options = ["{personID:>3} {first} {last}".format(**rec)
            for rec in records]
    layout=[[sg.Text(subheader,size=(30,1),
#           font='Lucida',justification='left'
            )],
            [sg.Listbox(values=options, select_mode='extended',
                key='CHOICE', size=(30,len(records)))],
            [sg.Button('SELECT',
#               font=('Times New Roman',12)
                ),
            sg.Button('CANCEL',
#                   font=('Times New Roman',12)
                    )
            ]]
    win =sg.Window(header,layout)
    e, v = win.read()
    win.close()
    if (e != "SELECT") or not v['CHOICE']:
        helpers.add2report(report, "Returning None")
        return
    else:
        personID = v['CHOICE'][0].strip().split()[0]
    helpers.add2report(report,
      "window in code.textual.choose returning..." +
      f"\n{repr(v['CHOICE'])}")
    for rec in records:
        if rec['personID'] == int(personID):
            return rec


def selectP_record(header_prompt="Provide hints:",
                    subheader="make a choice",
                    report=None):
    """
    Prompts 1st for hints and then to select.
    Returns a person record or None.
    """
    helpers.add2report(report,
            "Entering code.textual.selectP_record")
    choices = people_choices(header_prompt=header_prompt,
                            report=report)
    if choices:
        data = choose(choices,
                header=subheader,
                report=report)
        if data:
            helpers.add2report(report,
                "code/textual.selectP_record returning " +
                "(1st 3 key value pairs):..")
            for key, value in data.items():
                helpers.add2report(report, f"{key}: {value}")
#               if key == 'suffix': break  # no idea why!
            return data
        else:
            helpers.add2report(report,
            "code/textual.selectP_record 2nd stage failure.")
            return
    else:
        helpers.add2report(report,
            "code/textual.selectP_record 1st stage failure.")


def test_create_dem_file():
    data = dict(
      first= "Alex",
      last= "Kleider",
      suffix=  "",
      phone= "phone",
      address= "street",
      town= "Bo",
      state= "CA",
      postal_code= "94924",
      country= "usa",
      email= "alex@kleider.ca",
      )
#   for key, value in data.items():
#       print(f"  {key}: {value}")
    report=['creating dem file',]
    create_dem_file(data, report=report)
    print(report)


def main1():
    report = ['Report: ', ]
    data = get_demographics(report=report)
    if data:
        print("Data collected:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        _ = input("To continue hit the 'Enter' key... ")
    else:
        print("no data entered")
    yn = input("Create a '..Dem.txt' file? (y/n) ")
    if yn and yn[0] in "yY":
        create_dem_file(data, report=report)

def test_choose():
    options =['1 Alex Kleider',
            '2 Randy Rush',
            '3 Don Murch', ]
    while True:
        yn = input("\nRun test_choose? (y/n)")
        report = []
        if yn and yn[0] in 'yY':
            ret = choose(options, report=report,
                        header="[X] to abort, CANCEL to begin again",
                        subheader="Select your choice.")
            for line in report: print(line)
        else:
            break


def pick_person(header="CHOOSE ONE",
                subheader="Pick a person", font=font):
    """
    Returns a person record from the People table
        or None if user chooses to abort using [X].
    Used to obtain a record
    [X] ==> Returns None
    CANCEL ==> goes around again
    empty list ==> same as CANCEL
    If all goes according to plan:
    """
    while True:
        start_over = False
        # 1st collect the 'hints' ==> data:
        fields = routines.keys_from_schema(
                        "People", brackets=(1,7))
        layout = [[sg.Text(f_name), sg.InputText()]
                        for f_name in fields  ]
        layout.append([sg.Button('OK'),
                            sg.Button('Cancel')])
        window = sg.Window(
            'Enter hints using "%" as wild cards:',
            layout, font=font)
        while True:
            data = None
            event, values = window.read()
            print(f"event: {repr(event)}")
            if event == 'OK':
                if not values:  # could be an empty list
                    print("Got an empty list; try again.")
                    continue
                data = {}
                for n in range(len(values)):
                    data[fields[n]] = values[n]
                break  # got what we want!
            elif event == None:  # when user hits the [X]
                return
            elif event == 'Cancel':
                start_over = True
                break
            else:
                print("Unexpected event!")
                assert False
        window.close()
        if start_over: continue
        query_lines = [
            "Select personID, first, last, suffix",
                "from People where ", ]
        additional_lines = []
        if data['first']:
            additional_lines.append(
                f"""first like "{data['first']}" """)
        if data['last']:
            additional_lines.append(
                f"""last like "{data['last']}" """)
        if data['suffix']:
            additional_lines.append(
                f"""suffix like "{data['suffix']}" """)
        if not additional_lines:
            print("No clues provided; going again")
            continue
        additional_lines = " AND ".join(additional_lines)
        query_lines.append(additional_lines)
        query = ' '.join(query_lines)
        query = query+';'
#       _ = input(query)
        ret = routines.fetch(query, from_file=False)
        if not ret: continue
#       _ = input(repr(ret))
#       for item in ret:
#           print(item)
        choices = ["{0!s:>3} {1:} {2:} {3:}".format(*item) 
            for item in ret]

        #define layout
        layout=[[sg.Text(subheader,size=(30,1),
                )],
                [sg.Combo(choices,
                    default_value=choices[0],
                    key='choice')],
                [sg.Button('SELECT',
                    ),
                sg.Button('CANCEL',
                        )
                ]]

#       layout=[[sg.Text(choice), sg.InputText()]
#               for choice in choices]
#       layout.append([sg.Button('OK'),
#           sg.Button('Cancel')])
        #Define Window
        win =sg.Window(header,layout)
        #Read  values entered by user
        e, v = win.read()
        #close first window
        win.close()
        #access the selected value in the list box
        #and add them to a string
#       print(f"e returns {e}")
        if e == "CANCEL":
            continue
        elif e == None:
            return
        else:
    #       print("you chose: ",end='')
    #       print(repr(v['choice']))
            return routines.get_rec_by_ID(
                int(v['choice'].split()[0]))

def test_pick_person():
    while True:
        record = input(repr(pick_person()))
        print(repr(record))
        yn = input("Continue? (y/n) ")
        if not (yn and yn[0] in 'yY'):
            break

def menu(options, headers=["Main Menu", "Make a Choice"],
        report=None):
    """
    <options> is a dict/mapping (key/value pairs):
      keys are strings representing items from which to choose.
      Returned is the object/value corresponding to key chosen
        Note: values can be functions!
    Returns None if user aborts/no key is chosen.
    <headers> self explanatory (a header and a subheader)
    <report> if provided must be an iterable to which strings
    representing progress (or lack there of) are appended.
    """
    helpers.add2report(report, "Entering code/textual.menu...")
    keys = [key for key in options.keys()]
    layout = [
        [sg.Text(headers[1], size=(30,1),)],
        [sg.Listbox(values=keys, select_mode='extended',
            key='CHOICE', size=(30, len(options)))],
        [sg.Button('SELECT',), sg.Button('CANCEL'),]
            ]
    win = sg.Window(headers[0], layout)
    e, v = win.read()
    win.close()
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        helpers.add2report(report,
            f"Cancelled or no choice made; aborting {headers[0]}")
        if report: print(report[-1])
        return
#   _ = input(repr(v))
    ret = options[v['CHOICE'][0]]
    helpers.add2report(report,
        f"...code/textual.menu() returning {repr(ret)}")
    return ret

def test_menu():
    res = menu(dict(
        choice1="f1", choice2="f2", choice3="f3"),
            headers=["Main Menu", "Choosing strings"])
    _ = input(repr(res))
    def f1():
        print("f1 chosen")
    def f2():
        print("f2 chosen")
    def f3():
        print("f3 chosen")
    res = menu(dict(choice1=f1, choice2=f2, choice3=f3))
    _ = input(repr(res))
    if res:
        res()

def test_selectP_record():
    report = []
    while True:
        res = selectP_record(header_prompt="Provide hints",
                subheader="make a choice", report=report)
        if not res:
            print(f"selectP_record returned {repr(res)}")
        else:
            print("selectP_record returning the following...")
            for key, value in res.items():
                print(f"key: {repr(key)}, value:{repr(value)}")
        yn = input("Again?? (y/n): ")
        if not (yn and yn[0] in "yY"):
            break
#   _ = input("\nReport follows...")
#   print('\n'.join(report))


def test_edit_person_status():
    person_data = {'personID': 97,
                      'first': 'Alex',
                       'last': 'Kleider',
                     'suffix': '',
                    }
    fields = ('statusID', 'begin', 'end', )
    query = edit_person_status(person_data, fields,
        fstring="Member: {personID:>3} {first} {last} {suffix}")
    if not query:
        print("test_get_mode ==> invalid")
        return
    else:
        print("test_get_mode ==>")
        print(query)


def test_get_fields4():
    fields = ['statusID', 'begin', ]
    ret = get_fields4(person_data, fields)
    if not ret:
        print("invalid")
    else:
        for key, value in ret.items():
            print(f"{key}: {value}")

def test_get_fields():
    ret = get_fields(
        'first, last, address'.split(', ') )
    if isinstance(ret, dict):
        for key, value in ret.items():
            print(f"{key}: {value}")
    elif isinstance(ret, type(None)):
        print("None was returned")
    else:
        assert False


def test_a_show_stati():
    a_show_stati(f2run)
    print("Window has been closed.")


def test_pick():
    report=["Report:", ]
    print("====Returned by <pick>====")
    print(pick("""SELECT P.personID, P.last, P.first, P.suffix,
            Ps.statusID, PS.begin, PS.end 
        FROM Person_Status AS PS
        JOIN People AS P
        WHERE P.personID = PS.personID
        AND P.personID > 225;""",
        ("{personID:>3d} {last}, {first} {suffix}" +
        " {statusID} {begin} {end}"),report=report))
    print("=====Report follows======")
    for line in report:
        print(line)

def ck_yes_no():
    while True:
        if yes_no("query 2 run"):
            print("returned true")
        else:
            print("returned false")
        yn = input("Again?? (y/n): ")
        if not (yn and yn[0] in "yY"):
            break

def ck_get_demographics():
    data = get_demographics(
            report=["ck_get_demographics report"],
            applicant=True)
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(repr(data))


if __name__ == "__main__":
    ck_get_demographics()
#   ck_yes_no()
#   test_pick()
#   show_fonts()
#   test_a_show_stati()
#   test_get_fields4()
#   test_get_fields()
#   test_edit_person_status()
#   test_selectP_record()
#   test_people_choices()
#   test_choose()
#   test_pick_person()
#   test_create_dem_file()
#   main1()
#   test_menu()
#   test_cora()

