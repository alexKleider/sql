#!/usr/bin/env python3

# File: helpers.py

"""
Helper functions (initially developed for the Club/Utils repo
but now used in the following places unified by hard linking.)
This file appears in
    ~/Git/Club/Utils
    ~/Git/Lib/code
    ~/Git/Sql/code
TO DO: use uname -a to get system information
"""

import os
import sys
import shutil
import csv
import json
import time
import datetime
import functools
import collections
#from pathlib import Path

nowasint = int(time.time())
date_template = "%b %d, %Y"
date_w_wk_day_template = "%a, %b %d, %Y"
date_year_template = "%y"
today = datetime.datetime.today()
# sixdigitdate = today.strftime("%y%m%d")
eightdigitdate = today.strftime("%Y%m%d")
eightdigitdate4filename = today.strftime("%Y-%m-%d")
timestamp = today.strftime(         "%Y-%m-%d_%H:%M")
timestamp4filename = today.strftime("%Y-%m-%d_%H-%M")
month = today.month
this_year = today.year
date = datetime.datetime.strptime(
        today.strftime(date_template),
        date_template
            ).strftime(date_template)
N_FRIDAY = 4  # ord of Friday: m, t, w, t, f, s, s
              # should instead use rbc.Club.N_FRIDAY???
FORMFEED = chr(ord('L') - 64)  # '\x0c'

CURRENT_CENTURY = '20'


def eightdigitentry(prompt):
    """
    Forces input of an 8 digit entry.
    Used for YYYYmmdd date entries.
    """
    while True:
        entry = input(prompt)
        if entry.isdecimal() and len(entry)==8:
            return entry
        else:
            print("Must be an eight digit entry!")


def date_entry_w_default(prompt_preface=''):
    """
    new version of above: provides for a default of today.
    Returns a valid 8 digit string or None
    """
    while True:
        if not prompt_preface: prompt_preface = "New date "
        today = eightdigitdate
        try:
            new_date = input(
                f"{prompt_preface} (Rtn to accept default: {today},"
                +"\nCtl-C to quit, or"
                +"\nenter other date): ")
        except KeyboardInterrupt:
            return
        if len(new_date) == 0:
            new_date = today
        if not (new_date.isdigit()
                and
                (len(new_date) == 8)):
            print(
            f"'{new_date}' is an invalid date. Must be 8 digits")
        else:
            return new_date


def adjustyrby(yr, n):
    return str(int(yr[:4])+n) + yr[4:]

def get_os_release():
    with open('/etc/os-release', 'r') as info:
        assignments = info.read()
    return assignments.split('\n')[0].split('=')[1][1:-1]


def verify(notice, report=None):
    """
    Print notice and call sys.exit() if response does not begin with
    'y' or 'Y'.
    If report is set, it is printed before sys.exit() is called.
    Returns True if sys.exit() is not called.
    """
    response = input(notice)
    if not (response and response[0] in 'yY'):
        if report:
            print(report)
        sys.exit()
    else: return True

def content(file_name):
    """
    Assumes <file_name> is the name of a text file;
    Returns its content as a single string.
    """
    try:
        with open(file_name, 'r') as stream:
            return stream.read()
    except FileNotFoundError as err:
        print("OS error:", err)
        print(f"file {file_name} not found")
        raise

def equal_float(a, b):
    """
    compares floats for equality to limit of machine's accuracy
    # from Mark Summerfield
    """
    return abs(a - b) <= sys.float_info.epsilon


def get_attributes(r):
    """
    """
    return sorted([attribute for attribute in dir(r)
            if not attribute.startswith('__')])

#--------

def present_listing4approval(keys, values):
    """
    Returns a list of strings: "Key: Value"
    """
    d = {key: value for key, value in zip(keys, values)}
    return [f"    {key}: {value}" for key, value in d.items()]

def test_present_listing4approval():
    keys = ['first', 'last', 'suffix',]
    values= ['Alex', 'Kleider', 'MD',]
    prompt = ['Is the following OK...',]
    prompt.extend(present_listing4approval(keys, values))
    prompt.append("....y/n: ")
    _ = input("\n".join(prompt))
#--------

def check_dir_exists(directory, create=True):
    """
    Check for a file called <directory>:
    If it already exists:
        If it is not a directory: report and abort!
        If it exists and is a directory:
            report what's in it & offer to abort.
        Report as to its contents: empty or not.
    if it doesn't exist:
        if <create>: create it,
        else: offer to create it.
    Report results and ask if to continue.
    """
    if os.path.exists(directory):
        # check that it is a directory
        if os.path.isdir(directory):
            print(f"Directory {directory} exists.")
            # report if it's empty or contains file(s)
    else:  # no such file:
        yn = input(
    f"Directory {directory} does not exist! Create it? (y/n) ")
        if yn and yn[0] in 'yY':
            os.mkdir(directory)


def report_if_file_exists(file_name):
    """
    Report to the user if a file called <file_name>
    exists and if it is (or isn't) empty.
    """
    pass


def check_dir(directory, delete=False):
    """
    Parameter <file_names> may be one name or a sequence of names.
    For each- check with user if ok to delete or overwrite.
    Aborts program execution if permission is not granted.
    Does not itself do any deletion unless delete is set to True.
    """
    if isinstance(file_names, str):
        file_names = (file_names, )
    for f in file_names:
        if os.path.exists(f):
            response = input(
                    "'{}' exists! Over write &/or delete it?(y/n) "
                    .format(f))
            if not(response and response[0] in 'yY'):
                print('Aborting program execution.')
                sys.exit()
            elif delete:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                elif os.path.isfile(f):
                    os.remove(f)

def check_before_deletion(file_names, delete=False):
    """
    Parameter <file_names> may be one name or a sequence of names.
    For each- check with user if ok to delete or overwrite.
    Aborts program execution if permission is not granted.
    Does not itself do any deletion unless delete is set to True.
    """
    if isinstance(file_names, str):
        file_names = (file_names, )
    for f in file_names:
        if os.path.exists(f):
            response = input(
                    "'{}' exists! Over write &/or delete it?(y/n) "
                    .format(f))
            if not(response and response[0] in 'yY'):
                print('Aborting program execution.')
                sys.exit()
            elif delete:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                elif os.path.isfile(f):
                    os.remove(f)


def get_first_friday_of_month(date=None):
    """
    Accepts a date or uses current date if None is provided.
    Returns a datetime.date object representing the
    next first Friday of the month.
    """
    if not date:
        date = datetime.date.today()
    year = date.year
    month = date.month
    for d in range(1, 8):  # range => 1..7 covering first week
        day = datetime.date(year, month, d)
        if day.weekday() == N_FRIDAY:
            return day


def next_first_friday(today=datetime.date.today(),
                      exclude=False):
    """
    If <exclude> result will never be Jan 1
    Jan 8th will be returned.
    Returns a string (formated date.)
    """
    year = today.year
    month = today.month
    date = get_first_friday_of_month(today)
    if exclude:
        if date.month == 1 and date.day == 1:
            date = date + datetime.timedelta(days=7)
    if date < today:
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        date = get_first_friday_of_month(
            datetime.date(year, month, 1))
        if exclude:
            if date.month == 1 and date.day == 1:
                date = date + datetime.timedelta(days=7)
    return date.strftime(date_w_wk_day_template)


def club_year(which='this', now=datetime.date.today()):
    if which == 'last':
        n = -1
    elif which == 'this':
        n = 0
    elif which == 'next':
        n = 1
    else:
        print("Invalid parameter given to helpers.club_year()")
        sys.exit()
    if now.month > 6:
        return "{}-{}".format(now.year + n, now.year + n+1)
    else:
        return "{}-{}".format(now.year + n -1, now.year + n)


def expand_date(date_string):
    """
    Assumes date_string is in form yymmdd or yyyymmdd;
    Returns date in 'yyyy-mm-dd' format
    or "BAD DATE" if len(date_string) != 6 or 8.
    """
    if len(date_string) == 6:
        year = '{}{}'.format(CURRENT_CENTURY, date_string[:2])
    elif len(date_string) == 8:
        year = date_string[:4]
    else:
        print("Error: len(date_string) must be 6 or 8.")
        return 'BAD DATE'
    return '{}-{}-{}'.format(year, date_string[-4:-2],
                             date_string[-2:])


def get_datestamp(date=None):
    """
    Returns a string (for postal letters,) in the format 'Jul 03, 1945'.
    If <date> is provided it must be type datetime.datetime or
    datetime.date.  If not provided, today's date is used.
    """
    if date:
        if (isinstance(date,datetime.date)
            or isinstance(date, datetime.datetime)):
            d = date
        else:
            print("helpers.get_datestamp got a bad argument")
            sys.exit()
    else:
        d = datetime.date.today()
    return d.strftime(date_template)


def print_args(args, argument):
    """
    If args[argument] is True: print all the argument values.
    This works well with docopt when trying to debug.
    Screen width (number of columns) and height (number of rows) are
    assumed to be 80 and 24 unless defined by args['-w'] and/or
    args['r'] all respectively.
    """
#   print("Entering helpers.print_args")
    if args[argument]:
#       print(
#       "helpers.print_args' 2nd param evaluates 'True'")
        if '-w' in args.keys(): max_width = int(args['-w'])
        else: max_width = 80
        if '-r' in args.keys(): max_height = int(args['-r'])
        else: max_height = 24
        res = sorted(["{}: {}".format(key, args[key]) for key in args])
#       print(res)
        ret = tabulate(res, max_width=max_width, separator='   ')
        row_number = 0
        for row in ret:
            row_number += 1
            if row_number > max_height:
                row_number = 1
                _ = input("..any key to continue: ")
            print(row)
#       print("Got to here!!")
        response = input("...end of ## arguments. Continue? ")
        if not (response and response[0] in 'yY'):
            sys.exit()
    else:
#       print(
#       "helpers.print_args' 2nd param evaluates 'False'")
        pass  # no nothing if args['argument'] ==> False.


def print_usage_and_options(docstring):
    """
    Yet to be implemented: check that docstring contains
    both a Usage and an Options section.
    """
    uline = oline = -1
    doc_lines = docstring.split('\n')
    for n in range(len(doc_lines)):
#       _ = input("Line is '{}'".format(doc_lines[n].strip()))
        if doc_lines[n].strip() == "Usage:":
#           print("found usage @line {}".format(n))
            uline = n
        if doc_lines[n].strip() == "Options:":
#           print("found options @line {}".format(n))
            oline = n
            break
#       print("didn't find usage &/or options")
    if uline == -1 or oline == -1:
        print("Missing 'Usage' &/or 'Options' section.")
        sys.exit()
    print('\n'.join(doc_lines[uline:(oline-1)]))


def my_print(s, outf):
    with open(outf, 'w') as outfile:
        for item in sorted(s):
            outfile.write("{}\n".format(item))

class Rec(dict):
    """
    Each instance is a (deep!) copy of rec (a dict)
    and is callable (with a formatting string as a parameter)
    returning the populated formatting string. Suitable for
    displaying the record &/or when one wants to have the record
    modified without changing the original record (as when passed
    by reference!!)
    """
    def __init__(self, rec):
#       self = dict(rec)  # this should work but doesn't!!
        for key, value in rec.items():   #} use this method in
            self[key] = value            #} place of what's above

    def __call__(self, fstr):
        return fstr.format(**self)


def collect_last_first_keys(listofdicts):
    ret = []
    for rec in listofdicts:
        ret.append('{last},{first}'.format(**rec))
    return ret


def str_add(*args):
    total = 0
    for arg in args:
        if arg == '': arg = 0
        total += int(arg)
    return str(total)


def join_email_listings(*args):
    """
    Accepts any number of args, each of which must be a string
    consisting of emails, separated by comas if more than one,
    no spaces.
    Returned is a single string of "," separated emails
    with no duplicates suitable for placement into a 'cc'
    (or 'bcc') listing.
    NOTE: this is specific and should probably be moved
    to routines.py rather than be kept here.
    """
    res = []
    for arg in args:
        if arg:
            arg = arg.split(',')
            arg = [item.strip() for item in arg]
            res.extend(arg)
    return ','.join(sorted(set(res)))


def script_location():
    return os.getcwd()


def useful_lines(stream, comment="#"):
    """
    A generator which accepts an iterable of lines (strings.)
    Blank lines are ignored.
    If <comment> resolves to true, lines beginning with <comment>
    (after being stripped of leading spaces) are also ignored.
    <comment> can be set to <None> if don't want this functionality.
    Other lines are returned ("yield"ed) stripped of leading and
    trailing white space.
    """
    for line in stream:
        line = line.strip()
        if comment and line.startswith(comment):
            continue
        if line:
            yield line


def lists2sets(dict_with_iterable_values):
    """
    Converts list values (of a dict) into sets.
    """
    ret = {}
    for key in dict_with_iterable_values:
        ret[key] = set(dict_with_iterable_values[key])
    return ret


def keys_removed(a_dict, iterable_of_keys):
    """
    Returns a dict devoid of specified keys.
    """
    ret = {}
    unwanted = set(iterable_of_keys)
    for key in a_dict:
        if not key in unwanted:
            ret[key] = a_dict[key]
    return ret


def add2report(report, line_or_list, also_print=False):
    """
    This exact same code exists in code.routines from
    where it should be removed.
    Supports many routines which have a named 'report' param.
    NOTE: must be lists, NOT tuples!!
    ALSO NOTE: a list containing non strings would be a problem!!
    """
    if isinstance(report, list):
        if isinstance(line_or_list, str):
            report.append(line_or_list)
            if also_print: print(line_or_list)
        elif isinstance(line_or_list, list):
            report.extend(line_or_list)
            if also_print:
                for l in line_or_list: print(l)
        else:
            print("'add2report' paramater neither str nor list!")
            assert False

def save_db(new_db, outfile, key_list=None, report=None):
    """
    Saves data in <new_db> (a list of dicts) onto a csv file
    <outfile> with the keys specified by <key_list>.
    If <report> is specified, it must be a list of strings to
    which progress report is appended.
    If new_db is an empty list, does nothing
    """
    if not new_db: return
    if not key_list:
        key_list = new_db[0].keys()
    with open(outfile, 'w', newline='') as file_obj:
        writer = csv.DictWriter(file_obj,
                                fieldnames=key_list,
                                dialect='unix',
                                quoting=csv.QUOTE_MINIMAL,
                                )
        writer.writeheader()
        for record in new_db:
#           for line in [f"{key}: {value}" for key, value
#                   in record.items()]:
#               print(line)
            writer.writerow(record)
        alert = f"Data being sent to {file_obj.name}."
        add2report(report, alert,
                also_print=True)


def check_sets(s1, s2,
               header_in1st_not2nd="In 1st but not 2nd set:",
               header_in2nd_not1st="In 2nd but not 1st set:"):
    """
    Returns a listing of the differences between two sets.
    """
    ret = []
    in1st_not2nd = s1 - s2
    in2nd_not1st = s2 - s1
    if in1st_not2nd:
        add_header2list(header_in1st_not2nd,
                        ret, underline_char='-',
                        extra_line=True)
        ret.extend(sorted(in1st_not2nd))
    if in2nd_not1st:
        add_header2list(header_in2nd_not1st,
                        ret, underline_char='-',
                        extra_line=True)
#       my_print(in2nd_not1st, 'errors')
        ret.extend(sorted(in2nd_not1st))
    return ret


def format_dollar_value(value):
    if value > 0:
        return "${:,.2f}".format(value)
    elif value == 0:
        return "$0.00"
    elif value < 0:
        return "-${:,.2f}".format(abs(value))
    else:
        assert False, "Error in code.helpers.format_dollar_value."


def indent(text, n_spaces):
    """
    Helper function providing indentation for postal content.
    Can deal with either a list of strings ('lines')
    or one string ('lines' terminated by linefeeds.)
    In either case, returns a string.
    """
    assert type(n_spaces) == int, "Error in code.helpers.indent."
    indentation = ' ' * n_spaces
    if isinstance(text, str):
#       print("String found")
        lst = text.split('\n')
#       for s in lst:
#           print(s)
        return '\n'.join([indentation + line for line in lst])
    elif isinstance(text, list):
#       print("List found")
        return '\n'.join([indentation + line for line in text])
    else:
        print("helpers.indent(): Should NOT get here!")
        assert(False), "Error in code.helpers.indent."


def expand_array(content, n):
    """
    Assumes <content> is a sequence of <=n items.
    Returns a sequence of n itmes by padding both ends with empty
    strings.
    """
    if len(content) > n:
        print("ERROR: too many lines in <content>")
        print("    parameter of helpers.expand_array()!")
        assert False, "Error in code.helpers.expand_array."
    a = [item for item in content]
    while n > len(a):
        if n - len(a) >= 2:
            a = [''] + a + ['']
        else:
            a.append('')
    return a


def expand_string(content, n):
    a = content.split('\n')
    ret = expand_array(a, n)
    return '\n'.join(ret)


def expand(content, nlines):
    """
    Takes <content> which can be a list of strings or
    all one string with line feeds separating it into lines.
    Returns the same type (either string or list) but of <nlines>
    length, centered by blank strings/lines. If need an odd number
    of blanks, the odd one is at end (rather than the beginning.
    Fails if <content> has more than nlines.
    """
    if isinstance(content, str):
        return expand_string(content, nlines)
    else:
        return expand_array(content, nlines)


def add_header2list(header, list_, underline_char=None,
                    extra_line=True, indent=0):
    """
    Extends a list_ with a header preceded by an optional blank line
    and followed by an optional 'underline' composed of a specified
    character.
    Optional number of spaces to <indent>.
    """
    if extra_line:
        list_.append('')
    list_.append(" " * indent + header)
    if underline_char:
        list_.append(" " * indent + underline_char * len(header))


def add_sub_list(sub_header, sub_list, main_list,
                 underline_char="=", extra_line=True, indent=0):
    """
    Extends an existing <main_list> with a sorted version of
    <sub_list>.
    The added part is separated from the original by <separator> which
    must be a (possibly empty) list of strings- it defaults to a
    list of one empty string.
    """
    add_header2list(sub_header, main_list,
                    underline_char=underline_char,
                    extra_line=extra_line,
                    indent=indent)
    if indent:
        for item in sorted(sub_list):
            main_list.append(' ' * indent + item)
    else:
        main_list.extend(sorted(sub_list))


def prepend2file_name(word, file_name):
    """
    """
    head, tail = os.path.split(file_name)
    return os.path.join(head, ''.join((word, tail)))

def non_string_iterable(item, debug=False):
    if isinstance(item, str):
        if debug:
            print(f"{repr(item)} is a string; returning False")
        return False
    if isinstance(item, collections.abc.Iterable):
        if debug:
            print(f"{repr(item)} is a non string iterable")
        return True
    else: return False

def show_dict(d, extra_line=True, ordered=True, debug=False):
    """
    Returns a list of strings describing the dict key/values.
    <extra_line> if False: values same line as key.
    <ordered> if False: keys stay in order presented
    """
    lines = []
    keys = d.keys()
    if ordered:
        keys = sorted(keys)
    for key in keys:
        value = d[key]
        if non_string_iterable(value, debug=debug):
            value = ', '.join([val for val in sorted(value)])
        if extra_line:
            lines.append("{}\n\t{}\n".format(key, value))
        else:
            lines.append("{}: {}".format(key, value))
    return lines

def print_key_value_pairs(mapping):
    for line in show_dict(mapping,
                    extra_line=False, ordered=False):
        print(line)


def get_fieldnames(csv_file: "name of csv file", report=True
        ) -> "list of the csv file's field names":
    """
    Returns the field names of the csv file named.
    """
    with open(csv_file, 'r', newline='') as file_object:
        if report:
            print('DictReading file "{}"...'
                    .format(file_object.name))
        dict_reader = csv.DictReader(file_object, restkey='extra')
        return dict_reader.fieldnames


def dump2csv_file(listing, keys=None,
                         file_name="new_csv.csv"):
    """
    <listing> can be a list of iterables or a list of dicts
    in which case no need for the <keys> parameter.
    """
    if not len(listing) > 0:
        print("Nothing to store (code/helpers.dump2csv_file).")
        return
    with open(file_name, 'w', newline='') as outf:
        if isinstance(listing[0], dict):
            keys = [key for key in listing[0].keys()]
            writer = csv.DictWriter(outf, fieldnames=keys)
            writer.writeheader()
            for d in listing:
                writer.writerow(d)
        else:   # not dealing with a list of dicts!
            writer = csv.writer(outf)
            writer.writerow(keys)
            for iterable in listing:
                writer.writerow(iterable)


def store(collector, filename):
    """
    Sends contents of <collector> (json format) to <filename>.
    """
    with open(filename, 'w') as stream:
        stream.write('\n'.join(show_json_data(collector)))
        print(f'Data written to {filename}')


def show_json_data(json_data, underlinechar=''):
    """
    Returns a human readable representation of <json_data> data
    as a list of lines (which can be '\n'.joined.)
    If underlinechar is specified, each key is underlined and
    preceeded by a blank line.
    """
    collector = []
    indent = 0

    def collect(json_data, indent=indent, collector=collector):
        if isinstance(json_data, dict):
            # if keys need to be sorted change code by replaceing the
            # next line with:
            # for key in sorted(json_data.keys()):
            for key in json_data:
                if underlinechar:
                    collector.extend(['', key, underlinechar*len(key)])
                else:
                    collector.append(key)
                collect(json_data[key], indent=indent+2)
        elif isinstance(json_data, list):
            for item in json_data:
                collect(item, indent, collector)
        else:
            collector.append(' '*indent+str(json_data))

    collect(json_data, indent=indent, collector=collector)
    return collector


def dump2json_file(data, json_file, verbose=True):
    """
    <json_file> if it exists will be overwritten!!
    """
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  json_file_obj.name))
        json.dump(data, json_file_obj, indent=2)


def add2json_file(data, json_file, verbose=True):
    """
    <data> will be appended to <json_file> (which will be created
    if it doesn't already exist.
    """
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as j_file:
            if verbose:
                print('Loading existing (json) data from "{}".'
                        .format(j_file.name))
            data2add = json.load(j_file)
            if not isinstance(data2add, list):
                warning = [
                f"Warning: Content of {json_file} is not a list.",
                "Perhaps it was simply an empty file."
                "Beginning with an empty list",
                "Original content, if any, will be lost!"
                ]
                for line in warning: print(line)
                yn = input("Continue? (y/n) ")
                if yn and yn[0] in 'yY':
                    data2add = []
                else:
                    sys.exit()

        data2add.append(data)
    else:
        data2add = [data, ]
    with open(json_file, 'w', encoding='utf-8') as j_file:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  j_file.name))
        json.dump(data2add, j_file, indent=2)


def get_json(file_name, report=None):
    """
    JSON reads 'file_name': clients expect a list of dicts.
    Provides optional reporting.
    """
    with open(file_name, 'r') as f_obj:
        add2report(report,
            f'Reading JSON file "{f_obj.name}".',
            also_print=True)
        return json.load(f_obj)


def longest(x, y):
    """
    """
    if len(x) > len(y):
        return x
    else:
        return y


def tabulate(data,
             display=None,   # a function
             alignment='<',  # left (<), right (>) or centered (^)
             down=True,  # list by column (down) or by row (default)
             max_width=145,
             max_columns=0,
             separator=' | ',  # minimum separation between columns
             force=0,
             usage=False,
             stats=False):
    """
    The single positional argument (<data>) must be an iterable, a
    representation of which will be returned as a list of strings
    which when '\\n'.join(ed) can be printed as a table.
    If <display> is provided it must be a function that, when
    provided with an element of data, returns a string
    representation.  If not provided, elements are assumed to have
    their own __repr__ and/or __str__ method(s).
    Possible values for <alignment> are '<', '^', and '>'
    for left, center, and right.
    <down> can be set to True if you want the elements to be listed
    down the columns rather than across each line.
    If <max_columns> is changed, it will be used as the upper limit
    of columns used. It is only effective if you specify fewer
    columns than would fit into <max_width> and any <force>
    specifiction will take precedence. (See next item.)
    <force> can be used to force groupings. If used, an attempt is
    made to keep items in groups of <force>, either vertically (if
    <down>) or horizontally (if not.)
    If both are specified, and if <force> is possible, <force> takes
    precedence over <max_columns>, otherwise <force> is ignored.
    If <usage> is set to True, the <data> parmeter is ignored and
    this document string is returned.
    If <stats> is set to True, output will show table layout but no table.
    """
    orig_max_col = max_columns
    if usage:
        print(tabulate.__doc__)
        return
    # Assign <display>:
    if alignment not in ('<', '^', '>'):
        return "Alignmemt specifier not valid: choose from '<', '^', '>'"
    if display:  # Map to a representable format:
        _data = [display(x) for x in data]
    else:  # Eliminate side effects.
        _data = [x for x in data]
    # Establish length of longest element:
    max_len = len(functools.reduce(
                  lambda x, y: x if len(x) > len(y) else y, _data))
    # Establish how many can fit on a line:
    n_per_line = (
            (max_width + len(separator)) // (max_len + len(separator)))
    # Adjust for max_n_columns if necessary:
    # If <down> then <force> becomes irrelevant but otherwise,
    # force takes precedence over max_columns but within limits
    # of n_per_line.
#   print("max_columns ({}) < n_per_line ({})?"
#           .format(max_columns, n_per_line))
    if down:             # In down mode:
        # <force> is irelevant to n_per_line.
        if (max_columns > 0) and (max_columns < n_per_line):
            n_per_line = max_columns
    else:
        if max_columns < force and force <= n_per_line:
            max_columns = 0
        if force > 1 and n_per_line > force:
            _, remainder = divmod(n_per_line, force)
            n_per_line -= remainder
            forced = True
#           print("2. n_per_line is {}.".format(n_per_line))
        else:
            forced = False
        if max_columns > 0 and n_per_line > max_columns:
            if forced:
                temp_n = n_per_line
                while temp_n > max_columns:
                    temp_n -= force
                if temp_n > 0:
                    n_per_line = temp_n
            else:
                n_per_line = max_columns
#               print("3. n_per_line is {}.".format(n_per_line))
    if down:  # Tabulating downwards.
        column_data = []
        n_per_column, remainder = divmod(len(_data), n_per_line)
        if remainder:
            n_per_column += 1
        if force > 1:
            _, remainder = divmod(n_per_column, force)
            if remainder:
                n_per_column += force - remainder
        for j in range(n_per_column):
            for i in range(0, len(_data), n_per_column):
                try:
                    appendee = _data[i+j]
                except IndexError:
                    appendee = ''
                column_data.append(appendee)
        _data = column_data
    else:  # Tabulating accross so skip the above:
        pass
    if stats:
        return("Alignment={}, down={}, force={}, maxCol={}, n={}"
               .format(
                   alignment, down, force, orig_max_col, n_per_line))

    new_data = []
    row = []
    for i in range(len(_data)):
        if not (i % n_per_line):
            new_data.append(separator.join(row))
            row = []
        try:
            appendee = ('{:{}{}}'.format(_data[i],
                                         alignment, max_len))
        except IndexError:
            appendee = ('{:{}{}}'.format('', alignment, max_len))
        row.append(appendee)
    if row:
        new_data.append(separator.join(row))
    while not new_data[0]:
        new_data = new_data[1:]
    new_data = [item.strip() for item in new_data]
    return new_data


def send2file(text, filename, silent=False):
    """
    Write <text> to <filename> (silently (or not))
    <text> must be either a string or a list of strings.
    """
    if not silent:
        print(f"Sending text to {filename} ...")
    if isinstance(text, list):
        text = '\n'.join(text)
    with open(filename, 'w') as stream:
        stream.write(text)
    if not silent:
        print(f"... write to {filename} successfull.")


def output(data, destination=None, announce=True):
    """
    Sends data (text) to (a file called) <destination>
    (which defaults to stdout.)
    """
    if not destination:
        print(data)
    else:
        with open(destination, "w") as fileobj:
            fileobj.write(data)
            if announce:
                print('Data written to "{}".'.format(fileobj.name))

def clarify_cc(s, word2remove='sponsors'):
    """
    Assumes <s> is a string /w or /wo commas (but no blank spaces.)
    Splits the string on the commas(",") and looks for <word2remove>.
    Returns a 2-tuple:
        1st item: Boolean => presence of <word2remove>.
        2nd item: a list (possibly empty) of any other entries...
            (expect a listing of email addresses or an empty list.)
    """
    removed = False
    res = s.split(',')
    if word2remove in res:
        res.remove(word2remove)
        removed = True
    return (removed, res)


def tofro_first_last(name, as_key=True):
    """
    Parameter <name> is parsed and
    if of the form "John Doe":
        returns "Doe,John", or
            Doe, John if as_key==False
    if of the form "Doe, John" or "Doe,John":
            "John Doe" is returned.
    """
    if ',' in name:
        last, first = name.split(',')
        return f"{first.strip()} {last.strip()}"
    else:
        first, last = name.split()
        if as_key:
            return f"{last},{first}"
        else:
            return f"{last}, {first}"


def key2first_last(name):
    first, last = name.split(',')
    return f"{first} {last}"


def loose_trailing_empty_strings(list_of_strings):
    if list_of_strings:
        while not list_of_strings[-1]:
            list_of_strings = list_of_strings[:-1]
    return list_of_strings


def loose_spaces(line):
    words = line.split()
    return ''.join(words)


def add_fields(fieldnames, csv_file, prefix='new_'):
    """
    <csv_file> field_names must be a subset of <fieldnames>.
    Output has the same data but with blank entries for
    any field name not previously present.
    Output goes to a file with the same name prefixed by <prefix>
    (which can be set to an empty string in which case the file is
    replaced!)
    Data is temporarily stored in memory so beware if files are huge!
    """
    data = []
    with open(csv_file, 'r',
            encoding='utf-8', newline='') as instream:
        reader = csv.DictReader(instream)
        field_names = reader.fieldnames
        if not set(field_names).issubset(fieldnames):
            print("Assertion failed in helpers.add_fields!")
            sys.exit()
        for rec in reader:
            new_rec = {}
            for key in fieldnames:
                new_rec[key] = ''
            for key in rec.keys():
                if not rec[key]: rec[key] = ''
                new_rec[key] = rec[key]
            data.append(new_rec)
    if prefix:
        csv_file = prefix + csv_file
    with open(csv_file, 'w', newline='')as outstream:
        writer = csv.DictWriter(outstream,
                                fieldnames,
                                lineterminator='\n')
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def append_csv_data(new_info_csv, csv_file, zero=False):
    """
    Appends what is in <new_info_csv> file to
    what's already in <csv_file>.
    Field names (or just number of them?) must match.
    Returns field names taken from first parameter.
    If <zero> data (but not headers (fieldnames)) is removed from
    <new_info_csv>.
    ## Tested in Sandbox ##
    """
    field_names = ''
    with open(new_info_csv, 'r') as instream:
        reader = csv.DictReader(instream)
        field_names = reader.fieldnames
        with open(csv_file, 'a') as outstream:
            writer = csv.DictWriter(outstream, fieldnames=field_names,
                                dialect='unix',
                                quoting=csv.QUOTE_MINIMAL,)
            for line in reader:
                writer.writerow(line)
    if zero:
        with open(new_info_csv, 'w') as outstream:
            writer = csv.DictWriter(outstream, fieldnames=field_names,
                                dialect='unix',
                                quoting=csv.QUOTE_MINIMAL,)
            writer.writeheader()
    return field_names


def modify_csv_data(csv_file, func=None, params=None, outfile=None):
    """
    <outfile> defaults to 'temp-'+<csv_file> in same directory.
    Data in <csv_file> (as modified by func if provided) is moved to
    outfile. <params> can be provided for func if needed.
    Returns the name of the outfile.
    """
    if not outfile:
        outfile = prepend2file_name('temp-', csv_file)
    with open(csv_file, 'r') as instream:
        reader = csv.DictReader(instream)
        fieldnames = reader.fieldnames
        with open(outfile, 'w') as outstream:
            writer = csv.DictWriter(outstream,fieldnames=fieldnames)
            writer.writeheader()
            for record in reader:
                if func:
                    if params:
                        writer.writerow(func(record, params))
                    else:
                        writer.writerow(func(record))
                else:
                        writer.writerow(record)
    return outfile


def compare_dicts(d1, d2,
            name1='first', name2='second'):
    """
    """
    ret = []
    keys1 = set([key for key in d1.keys()])
    keys2 = set([key for key in d2.keys()])
    only_in1 = keys1 - keys2
    only_in2 = keys2 - keys1
    if only_in1:
        ret.append(f"Only in {name1}:")
        for key in sorted(only_in1):
            values = sorted([value for value in d1[key]])
            ret.append(f"\t{key}: "+', '.join(values))
    if only_in2:
        ret.append(f"Only in {name2}:")
        for key in sorted(only_in2):
            values = sorted([value for value in d2[key]])
            ret.append(f"\t{key}: "+', '.join(values))
    return '\n'.join(ret)


def main():
    print("The month is '{}'.".format(month))
    print("'helpers.get_datestamp() returns '{}'."
          .format(date))

    print("'club_year(this)' returns '{}'."
          .format(club_year("this")))

    addresses = [
        "Alex Kleider\nPO Box 277\nBolinas, CA 94924",
        """Alex Kleider
PO Box 277
Bolinas, CA 94924""",
        ["Alex Kleider", "PO Box 277", "Bolinas, CA 94924"]]

    expanded = [expand(addr, 7) for addr in addresses]
    indented = [indent(addr, 4) for addr in addresses]

    for addr in expanded:
        print("--")
        print(addr)
    print("--")
    debugging_code = """
    print("--")
    for addr in indented:
        print("--")
        print(addr)
        print(repr(addr))
    print("--")
    for n in range(len(indented)-1):
        for i in range(len(indented[n])):
            if indented[n][i] != indented[n+1][i]:
                print("{} == {}".format(indented[n][i], indented[n+1][i]))
            else:
                print("{} == {}".format(indented[n][i], indented[n+1][i]))
        if len(indented[n]) != len(indented[n+1]):
            print("lengths are not equal")
        if indented[n] != indented[n+1]:
            print("The following are not equal:")
            print(repr(indented[n]))
            print("----")
            print(repr(indented[n+1]))
            print("----")
    """
    assert(indented[0] == indented[1]), "Error in code.helpers.main."
    assert(indented[1] == indented[2]), "Error in code.helpers.main."


def test_show_json_data():
    data = {"Chadwick, Michael": [["Mooring", 114]], "Churchman, Josh": [["Mooring", 114]], "Cowman, Tim": [["Mooring", 114]], "Differding, Gary": [["Mooring", 114]], "Ferraro, Joseph": [["Mooring", 138]], "Mann, Ed": [["Mooring", 114]], "Murch, Don": [["Mooring", 152]], "O'Connor, Daniel": [["Mooring", 138]], "O'Neil, Terry": [["Mooring", 132]], "Rodoni, Fred": [["Mooring", 114]], "Smith, Thornton": [["Mooring", 138]], "Swanson, Eric": [["Mooring", 126]], "Bettini, Rick": [["Dock", 75]], "Buckenmeyer, Robert": [["Dock", 75]], "Dixon, Rupert": [["Dock", 75]], "Ferlinghetti, Leonardo": [["Dock", 75]], "Finney, Scott": [["Dock", 75]], "Heffelfinger, Robert": [["Dock", 75]], "Krakauer, George": [["Dock", 75]], "Krieger, Nicholas": [["Dock", 75]], "Light, Mike": [["Dock", 75]], "MacDonald, Bob": [["Dock", 75]], "Martinelli, Chris": [["Dock", 75]], "McPhail, Jeff": [["Dock", 75], ["Kayak", 70]], "Norton, William": [["Dock", 75]], "O'Connor, Nick": [["Dock", 75]], "Smith, Peter": [["Dock", 75]], "Vantress, John": [["Dock", 75]], "Walker, Kirsten": [["Dock", 75]], "Barth, Doug": [["Kayak", 70]], "Cirincione-Coles, Kathryn": [["Kayak", 70]], "Griffith, Melinda": [["Kayak", 70]], "Martin, Monica": [["Kayak", 70]], "Mott, James": [["Kayak", 70]], "Pedemonte, Richard": [["Kayak", 70]], "Read, Don": [["Kayak", 70]], "Sawyer, Aenor": [["Kayak", 70]], "Straton, Joe": [["Kayak", 70]], "Thompson, Randall": [["Kayak", 70]], "Tremp, Dieter": [["Kayak", 70]]}
    print('\n'.join(show_json_data(data)))

####  menu related ...  ####

def get_menu_dict(items):
    """
    Returns a dict keyed by successive integers
    beginning with 1 (not zero!)
    """
    z = zip(range(1, len(items)+1), items)
    menu = dict()
    for key, item in z:
        menu[key] = item
    # remember: key is an int! (not a string)
    # '0' is reserved for Q)uit.
    return menu


def get_menu_response(items, header=None, incl0Q=True):
    """
    <items> a sequence of menu options
    <header>  line (if provided)to insert above the choices
    <incl0Q> == include a "0 to quit" 'choice'.
    It's up to client to deal with a "0 to quit" choice.
    Returns a 1 based integer
    """
    menu = get_menu_dict(items)  # see get_menu_dict doc_string
#   _ = input(menu)
    while True:
        if header: display = [header, ]
        else: display = []
        if incl0Q: display.append('  0: Q)uit')
        for key, value in menu.items():
            display.append(f"{key:>3}: {value}")
        print('\n'.join(display))
        if incl0Q: extra = " (or 'Q' to quit)"
        else: extra = ""
        response = input(f"Choice (must be an integer{extra}): ")
        if response and response[0] in "qQ":
            return 0
        try:
            response = int(response)
        except ValueError:
            print("Only an integer or 'q' or 'Q' allowed!")
            continue
        if incl0Q: lower_limit = 0
        else: lower_limit = 1
        if response>=lower_limit and response<=(len(items)+1):
#           _ = input(f"returning menu choice {response}")
            return response


def make_dict(keys, values):
    """
    Parameters are iterables of equal length.
    A dict is returned.
    Fails if lengths are not equal!
    """
    assert len(keys) == len(values), '\n'.join((
        'len(keys) != len(values) in helpers.make_dict.',
        f'keys: {keys}', f' values: {values}'))
    ret = {}
    for key, value in zip(keys, values):
        ret[key] = value
    return ret

def get_int(prompt='Enter an integer: ',
        blank=True,
        maxn=0):
    """
    Plagerized from "Python Projects" (2015)
    by Laura Cassell and Alan Gauld (p22-23)
    with modifications:
        i. if <blank>, will accept empty string returning 0)
       ii. <maxn> (if >0) is the highest number accepted.
      iii. will not accept a negative number
    """
    while True:
        n = input(prompt)
        if blank and not n:
            return 0
        try:
            n = int(n)
        except ValueError:
            print("Must enter an integer! Try again...")
            continue
        if n < 0:
            print("Must enter an integer >= 0! Try again...")
            continue
        if maxn and n > maxn:
            print(f"Integer must be <= {maxn}! Try again...")
            continue
        break
    return n

def choose_file_name(default=None):
    """
    """
    if default:
        print(f"Default file name is {default})")
        outfile = input("Enter file name (or blank for default): ")
        if not outfile:
            outfile = default
    else:
        outfile = input("Enter file name: ")
    return outfile


"""
Work on menu development
"""

def func1(): print("ran func1")
def func2(): print("ran func2")
def func3(): print("ran func3")
def func4(): print("ran func4")

proto_menu = {
        "name1": func1,
        "name2": func2,
        "name3": func3,
        "name4": func4,
        }

def choose_and_run(proto_menu,
            report=None,
           header=f"Choose 0..{len(proto_menu)}:",
            prompt="Choice: "):
    """
    <proto_menu> must be a dict:
        keys==choices
        values==functions
    <report> if provided must be a list (of strings)
    <header> & <prompt>: self explanatory
    """
    if isinstance(report, list):
        report.append(
            "Using helpers.choose_and_run to present a menu..")
    names = [name for name in proto_menu.keys()]
    menu = get_menu_dict(names)
    while True:
        if header:
            print(header)
        print("  0: Quit")
        for key, value in menu.items():
            print(f"{key:>3}: {value}")
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Must enter an integer " +
                  f"0..{len(proto_menu.keys())}: ")
            continue
        if choice == 0:
            print("Leaving menu!")
            break
        if choice in range(len(names)+1):
            return [
                func for func in proto_menu.values()
                ][choice-1](report=report)
        else:
            continue  # if choice > number of choices


def main():
    print(timestamp)
#   choose_and_run(proto_menu)
#   test_present_listing4approval()
    print(get_os_release())
#   print(f"sixdigitdate: {sixdigitdate}")
    print(f"eightdigitdate: {eightdigitdate}")
    print(
f"today: {today}; month: {month}; this_year: {this_year}; date: {date}")
    print("Module helpers compiles without error.")
#   main()
#   test_show_json_data()

def test_Rec():
    d1 = {'1': "Alex", '2': "June", '3': "Tanya", '4': "Kelly", }
    d2 = Rec(d1)
    print(d2)
    d2['5'] = "Isabella"
    print(d1)
    print(d2)
    print(d1 is d2)
    print(d2("Wife's name is {'2'}."))

def ck_date_entry():
    while True:
        date = date_entry_w_default("Choose date")
        if date == "00000000":
            break
        print(date)
        print()


if __name__ == "__main__":
#   main()
#   test_Rec()
#   ck_date_entry()
    print(f"today: {today}")
    print(f"date: {date}")
    print(f"eightdigitdate: {eightdigitdate}")
    print(f"eightdigitdate4filename: {eightdigitdate4filename}")

