#!/usr/bin/env python3

# File: parse_applicant_data.py

"""
Still a work in progress to move info in old DB (applicants.txt)
into the Applicants table of the new SQL data base.
Should be moved into the OnceOnly directory.
"""

from code import helpers

applicant_spot = '/home/alex/Git/Club/Data/applicants.txt'

APPLICANT_DATA_FIELD_NAMES = (
    "first", "last", "suffix", "status",
    "app_rcvd", "fee_rcvd",   #} date (or empty
    "meeting1", "meeting2", "meeting3",      #} string if event
    "approved", "dues_paid",  #} hasn't happened.
    "notified",               # empty strings if not available
#   "sponsor1", "sponsor2",
    )
MEETING_DATE_NAMES = APPLICANT_DATA_FIELD_NAMES[6:9]

STATUS_KEY_VALUES = {
    "a-": "Application received without fee", #0
    "a" : "Application complete but not yet acknowledged",
                # temporary until letter of welcome is sent
    "a0": "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ai": "Inducted, needs to be notified",  # temporary until letter
    "ad": "Inducted & notified, membership pending payment of dues",
    "av": "Vacancy ready to be filled pending payment of dues",
    "aw": "Inducted & notified, awaiting vacancy", #7 > #8
    "am": "New Member",  # temporary until congratulatory letter.
    "be": "Email on record being rejected",   # => special notice
    "ba": "Postal address => mail returned",  # => special notice
    "h" : "Honorary Member",                             #10 > #12
    'm' : "Member in good standing",
    'i' : "Inactive (continuing to receive minutes)",
    'r' : "Retiring/Giving up Club Membership",
    't' : "Membership terminated (probably non payment of fees)",
            # a not yet implemented temporary
            # status to trigger a regret letter
    "w" : "Fees being waived",  # a rarely applied special status
    'z1_pres': "President",
    'z2_vp': "VicePresident",
    'z3_sec': "Secretary of the Club",
    'z4_treasurer': "Treasurer",
    'z5_d_odd': "Director- term ends Feb next odd year",
    'z6_d_even': "Director- term ends Feb next even year",
    'zae': "Application expired or withdrawn",
    'zzz': "No longer a member"  # not implemented
            # may use if keep people in db when no longer members
    }
STATI = sorted([key for key in STATUS_KEY_VALUES.keys()])
SPECIAL_NOTICE_STATI = set(      # 'b' for bad!
    [status for status in STATI if status.startswith('b')])
APPLICANT_STATI = [              # 'a' for applicant!
    status for status in STATI if status.startswith('a')]
APPLICANT_SET = set(APPLICANT_STATI)


def move_date_listing_into_record(dates, record):
    """
    # used by applicant_data_line2record #
    <dates>: a listing (possibly incomplete) of relevant dates.
    <record>: a dict to which to add those dates by relevant key.
    returns the record
    """
    for key, index in (('app_rcvd',  0),
                       ('fee_rcvd',  1),
                       ('1st',       2),
                       ('2nd',       3),
                       ('3rd',       4),
                       ('inducted',  5),
                       ('dues_paid', 6)):
        try:
            record[key] = dates[index]
        except IndexError:
            record[key] = ''
            continue
    return record


def applicant_data_line2record(line):
    """
    # used only by populate_applicant_data #
    Assumes a valid line from the Data/applicant.txt file.
    Returns a dict with keys as listed in 
    Club.APPLICANT_DATA_FIELD_NAMES = (
        "first", "last", "suffix", "status",
        "app_rcvd", "fee_rcvd",   #} date (or empty
        "1st", "2nd", "3rd",      #} string if event
        "inducted", "dues_paid",  #} hasn't happened.
#       "sponsor1", "sponsor2",   # empty strings if not available
        )
    Note: terminates program if no dates are provided.
    """
    ret = {}
    for key in APPLICANT_DATA_FIELD_NAMES:
        ret[key] = ''
    parts = line.split('|')
    while not parts[-1]:  # lose trailing empty fields
        parts = parts[:-1]
    parts = [part.strip() for part in parts]
    names = parts[0].split()
    ret['first'] = names[0]
    ret['last'] = names[1]
    ret['suffix'] = ''
    if ret['last'] == "Murch_Jr":
        ret['last'] = "Murch"
        ret['suffix'] = 'Jr'
    dates = parts[1:]
    l = len(dates)
    if parts[-1].startswith("Appl"):
        dates = dates[:-1]  # waste the text
        special_status = "zae"  # see members.STATUS_KEY_VALUES
        l -= 1
    elif parts[-1].startswith("w"):
        dates = dates[:-1]
        special_status = "aw"
        l -= 1
    else:
        special_status = ''
    if l == 0:       # Should never have an entry /w no dates.
        print("Entry for applicant {}{} is without any dates."
                .format(names[0], names[1]))
        sys.exit()
    elif l == 1:               # one date listed
        status = "a-"
    elif l == 2:
        status = "a0"
    elif l == 3:
        status = "a1"
    elif l == 4:
        status = "a2"
    elif l == 5:
        status = "a3"
    elif l == 6:
        status = "ad"
    elif l == 7:
        status = "m"
    else:
        print("Entry for {}{} has an invalid number of dates."
                .format(names[0], names[1]))
        sys.exit()
    move_date_listing_into_record(dates, ret)
    if special_status:
        ret['status'] = special_status
    else:
        ret['status'] = status
    return ret

def applicant_data(source_file):
    """
    Returns data found in our old applicants.txt file
    (a list of records)
    """
    applicant_data = []
    with open(source_file, 'r') as stream:
        for line in helpers.useful_lines(stream, comment='#'):
            rec = applicant_data_line2record(line)
#           if (not(rec['status'] in APPLICANT_SET)
#           and not club.all_applicants):
#               continue
            applicant_data.append(rec)
#           name_key = "{last},{first}".format(**rec)
#           if rec['suffix']:
#               name_key = name_key + ' ' + rec['suffix']
    return applicant_data



def parse_sponsor_data_line(line):
    """
    # used by populate_sponsor_data #
    Assumes blank and commented lines have already been removed.
    returns a 2 tuple: (for subsequent use as a key/value pair)
    t1 is "last,first" of applicant (can be used as a key)
    t2 is a tuple of sponsors ('first last')
    eg: ('Catz,John', ('Joe Shmo', 'Tom Duley'))
    Fails if encounters an invalid line!!!
    """
    parts = line.split(":")
    sponsored = parts[0].strip()
    names = sponsored.split()
    name = '{},{}'.format(names[1], names[0])
    part2 = parts[1]
    sponsors = (parts[1].split(', '))
    sponsors = tuple([sponsor.strip() for sponsor in sponsors])
    return (name, sponsors)


def line_of_meeting_dates(applicant_datum):
    """
    Returns a string: comma separated listing of meeting dates.
    """
    dates = []
    for date_key in MEETING_DATE_NAMES:
        if applicant_datum[date_key]:
            dates.append(applicant_datum[date_key])
    return ', '.join(dates)

if __name__ == '__main__':
    print('Reading file "{}"...'.format(applicant_spot))
    data = applicant_data(applicant_spot)
    print("The following data has been collected:")
    header = "Keys are "
    keys = [key for key in data[0].keys()]
    print(header + ', '.join(keys))
    for datum in data:
        print([value for value in datum.values()])
