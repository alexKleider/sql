#!/usr/bin/env python3

# File: content.py

"""
Developed to serve as module by the same name served
the 'before SQL' version of membership management.

Rather than importing functions, they are referred to by
name and depend on a dict within the utils.Membership class
with those names as keys and the methods as values.

A number of 'dict's are being used:
    letter_bodies
    authors: ak, membership,
    content_types    # "which"
        each provides: {
            "subject":
            "from": authors["membership"],
#           'reply2': 'randolf@sonic.net'
            "body": letter_bodies["happyNY_and_0th_fees_request"],
            "post_script": a string,
            "funcs": [func_1, ..],
            "test": members.is_member, 
            "e_and_or_p": "one_only",
            },
    printers: X6505, HL2170, ...

Other items:
    email_header
    func: prepare_letter_template(which_letter, printer):
    func: prepare_email_template(which_letter):

Printing Letters:
Both the printer and the windowed envelope being used must be taken
into consideration.
"""

try: from code import club
except ImportError: import club

try: from code import helpers
except ImportError: import helpers

try: from code import routines
except ImportError: import routines

try: from code import members
except ImportError: import members

address_format = """{first} {last}{suffix}
{address}
{town}, {state} {postal_code}
{country}"""

letter_bodies_docstring = """
Some of these 'bodies' are subject to the format method
and those must have {{double}} parens for the format fields
that must be subsequently filled in by the '..._funcs'.
"""

# # single braces are for fields populated by the content_type data.
# # double braces fields are populated by the record data.

letter_bodies = dict(

    angie_print="""
The Bolinas Rod & Boat Club is facing a crisis!

Leadership positions are being vacated and need to be filled.

Our Secretary is retiring; we need at least a Vice President
and may need a President as well; Four of our directors are
ending their terms in February and it's unclear how many will
be willing to stay on for another two year term.

This letter is an urgent appeal for volunteers who might be
willing to stand for election to these important positions.
Important because the Club is facing challenges that it can
only meet if there is a complete and dedicated leadership.

If the Club falters and goes in a direction of which you don't
approve, members will have only themselves to blame for not
stepping up to provide guidance.

If willing to serve please nominate yourself. You can do so
by email (rodandboatclub@gmail.com) or post (94924-0148.)
The annual general meeting is coming up the first Friday of
February so time is running out.
""",

    find_enclosed="""
Please find enclosed.
""",

    for_testing="""
Blah, Blah-
more Blah blah

etc


May have as many 'extra's as required as long as each one
has a corresponding entry in the record dict (typically arranged
by the custom function.
""",

    bad_address="""
Mail sent to you has been returned.

We have your mailing address as :

{extra}

Please let us know if this should be corrected and, if so, to what.
""",

    feb_meeting="""

We have a special Bolinas Rod and Boat Club meeting coming up
{}.

Board members meet at 5pm.

The general meeting is scheduled for 6:00pm.
Election of Officers is the main agenda item.

Those with reservations[1]  are invited to stay for the
annual dinner to follow.

Come for the fun!
""".format(helpers.next_first_friday()),

    usps_minutes="""
Enclosed, please find the latest Club minutes.
Enjoy!
""",

    happyNY_and_0th_fees_request="""
A very Happy New Year to all members of the Bolinas Rod & Boat
Club!

Another friendly reminder that the Club maintains a membership
list on the 'Membership' section of the Club web site:
(rodandboatclub.com, password is 'fish'.) Please check it out
if you want to get in touch with a fellow member.
changes that should be made.

At this time you might be doing some financial planning for the
year; don't forget to include provisions for payment of Club dues
(and possibly fees as well.)  The following is included to help
you in this regard.  It's always acceptable to pay early and get it
behind you.{extra}

If the number is negative or zero, there'll be nothing due in June.
""",

    thank="""
This acknowledges receipt of your recent ${total} payment applied
to your account as it previously stood:
{before_statement}.
Thank you.

A statement of your current standing follows:
{statement}

All the best!
""",

    # Correction!!!
    correction="""
You recently received a statement of dues for the upcoming
({}) Club year. I believe the total was in error and the
corrected amount is indicated below.  You can pay it any
time although it isn't due until June.

If you have reason to believe this is in error, please let
me know[1].

My apologies for the confusion (caused by my ineptitude!)
{{extra}}""".format(helpers.club_year(which='next')),

    first_notice="""
This is a reminder that annual Club dues will be due in June.
That is still a ways out but some might like to know in advance
in order to be able to budget appropriately.  Advance warning
also benefits those that might be planning to be away for the
summer.

A statement of your dues (+/- fees) for the upcoming ({}) Club
year appears bellow.  (If you've any reason to believe that
our accounting might be in error, please let us know[1].)
If the total is zero (or negative) you're all paid up (or more
than paid up) for the upcoming year and we thank you.
{{statement}}""".format(helpers.club_year(which='next')),

    # Send with June minutes:
    June_request="""
We are now in the final month of this ({}) Club year and
annual dues (and fees where applicable) are due at the end
of the month.

This mailing is going out to all members so everyone can know
where they stand whether already paid up or not.
(If you've any reason to believe that our accounting might be
in error, please let it be known[1].)

Details are as follows:
{{statement}}""".format(helpers.club_year(which='this')),

    July_request="""
The new ({}) Club year has begun. Please send in your dues
(and any applicable fees) to the Bolinas Rod and Boat Club
at the address provided below.

If you've any reason to believe that our accounting might
be in error, please let it be known[1]. Also keep in mind
that if you have recently sent in a payment, it may not yet
have been processed. An acknowledgement letter is generally
sent when payments are processed.

Details are as follows:
{{statement}}""".format(helpers.club_year(which='this')),

    interim_request="""
Club records indicate that you have dues (and/or
applicable fees) outstanding as follows...

{extra}

If you've any reason to believe that our accounting might be
in error, please let it be known[1]. Otherwise, please send
in your remittance to the
    Bolinas Rod and Boat Club,
    PO Box 248, Bolinas, CA 94924.
at your earliest convenience.

Remember: by-laws dictate that membership is
terminated if dues are not paid by September 1st.
""",

    # Send in early August:
    August_mailing="""
As we enter the month of August it means you've already enjoyed
a month of Club membership and/or one or more of its benefits
for free but this could end soon if you don't take action!

Club records indicate that your dues (+/or other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if dues are not paid by Sept 1st.
Note that the date is Sept 1st, not the 15th as is sometimes
incorrectly quoted.

(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{statement}""",

    last_chance="""
If you haven't yet paid your Club dues (&/or other fees,) time
is running out. Membership is terminated if dues are not paid
by September 1st which is fast approaching.

Our treasurer, Angie Calpestri, asks that everyone be made aware
that fees can be easily paid using Venmo (details below.)

What follows is a statement of what Club records indicate must be
paid if membership is to continue.
{statement}""",

    # Send towards end of August:
    final_warning="""
Club records indicate that your dues (+/or other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if fees are not paid by Sept 1st.
(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{statement}""",

    bad_email="""
Emails sent to you at
    "{email}"
are being rejected.

Can you please help sort this out by contacting us
at rodandboatclub@gmail.com?

Thanks,""",

    waiting4application_fee=f"""
We've received your application which will be complete once the
application fee (${club.applicant_fee}) has been received.
You are now listed in the Club data base.

The process has begun!""",

    applicant_fee_pending="""
The Club is now in receipt of your application but there is
still the application fee to be submitted.

Once the Treasurer notifies me that it has come in, I will
communicate further.

In the mean time please keep in touch with your sponsors who
have the duty to shepherd you through the application process.
""",

    app_fee_received="""
Your application fee has been received so your application is
now complete!

As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

If they haven't already done so, please ask your sponsors to
inform you of the purpose and rules of the Club (as required by
our By-Laws.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in a six
month period.  You may attend as the guest of any member; your
sponsors are expected to introduce you.

Looking forward to seeing each other at future meetings held at
the Club: 83 Wharf Rd., Bolinas, CA 94924
""",

    new_applicant_welcome="""
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

If they haven't already done so, please ask your sponsors to
inform you of the purpose and rules of the Club (as required by
our By-Laws.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in a six
month period.  You may attend as the guest of any member; your
sponsors are expected to introduce you.

Looking forward to seeing each other at future meetings held at
the Club: 83 Wharf Rd., Bolinas, CA 94924
""",

    awaiting_vacancy="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

Unfortunately there is not currently a vacancy (since club
bylaws specify that membership must not be over 200.)

But don't despair!  You are certainly welcome to enjoy most
if not all of the privileges of membership until a vacancy
occurs at which time I will send you a request for payment of
dues and once paid you will become a full fledged member!

You're almost there; "as good as" for all intents and purposes!""",

    vacancy_open="""
It's my pleasure to report that a vacancy has come up and so
you can now become a member.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    request_inductee_payment="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of prorated dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    second_request_inductee_payment="""
Your application for Club membership was approved by the
Club Executive Committee and membership fees have been
requested but as yet not received.  Until payment is
received you are not yet a member.  This could create a
problem for the Exec committee since there are applicants
ready to take the spot that you would take if, but only if, the
dues are paid.

Please send a check for ${current_dues} to the Club
(address provided below.)""",


    # following will eventually be redacted in favour of
    # first_dues_payment_welcome

    welcome2full_membership="""
As Membership Chair, it is my pleasure to welcome you as a new
member to the Bolinas Rod and Boat Club!

As you may know, the Club has its own web site 'rodandboatclub.com'
which is password protected. The password is 'fish' and although
not a very closely guarded secret, please do not share it with non
members.  By clicking on the "Membership" tab, you can find a
listing of all your fellow members along with contact information.
Please have a look and if you see any inaccuracies please make it
known[1] so corrections can be made.

There is a wealth of history on our website: recordings of past
'marine moments' along with photos of events, and forms for renting
the club ~ lots to explore there.

Members can (upon payment of a $25 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  This provides fishermen
and boaters access to the docks (the use of which is a privilege
for which there is an extra fee- see Docks and Yards Chair Don
Murch about that) and also many take advantage of having this
access to spend time on the balcony enjoying views of the lagoon
and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the
web site: "Rules and Forms" and under that "Club Rentals".

Please contact your sponsors or reach out to me if you have any
questions about anything related to the Club. If I can't answer,
I'll try to find someone who can.

As you already know, general membership meetings are held on the
first Friday of each month @ 7:30. The February Annual General
meeting is an exception to this rule. You'll be receiving
announcements from the Club Secretary. Please come and attend
meetings and other functions to enjoy the camaraderie!""",

    first_dues_payment_welcome="""
Your dues payment of ${amt_paid} has been received so it is now
my pleasure, as Membership Chair, to welcome you as a new member
to the Bolinas Rod and Boat Club!

As you may know, the Club has its own web site 'rodandboatclub.com'
which is password protected. The password is 'fish' and although
not a very closely guarded secret, please do not share it with non
members.  By clicking on the "Membership" tab, you can find a
listing of all your fellow members along with contact information.
Please have a look and if you see any inaccuracies please let me
know so corrections can be made.

There is a wealth of history on our website: recordings of past
'marine moments' along with photos of events, and forms for renting
the club ~ lots to explore there.

Members can (upon payment of a $25 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  This provides fishermen
and boaters access to the docks (the use of which is a privilege
for which there is an extra fee- see Docks and Yards Chair Don
Murch about that) and also many take advantage of having this
access to spend time on the balcony enjoying views of the lagoon
and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the
web site: "Rules and Forms" and under that "Club Rentals".

Please contact your sponsors or reach out to me if you have any
questions about anything related to the Club. If I can't answer,
I'll try to find someone who can.

As you already know, general membership meetings are held on the
first Friday of each month @ 7:30. The February Annual General
meeting, held at 6pm, is an exception to this rule. You'll be
receiving announcements from the Club Secretary. Please come and
attend meetings and other functions to enjoy the camaraderie!""",

    expired_application="""
With considerable regret it is my duty to inform you of the
following:
It's been more than six months since your membership application
has been received and during that time you've failed to attend
the required three Club meetings. This causes your application to
expire.
If you still wish to be a member of the Bolinas Rod and Boat Club
the application process must begin again and I suggest you work
closely with your sponsors.""",

    retirement_from_club="""
Your wish to retire from Club membership has been noted.

I know I speak for all members in saying we're sorry to see you go
and wish you all the best in the future.""",

    membership_termination="""
Since your membership dues have not been received by the Sept 1st
dead line set by the club by-laws, it is my sad duty to inform
you that your membership has been terminated.  Should you wish
to become a member again, it'll be necessary for you to reapply.

Let me add my own personal sentiment of regret that you have
chosen to leave the club.

If you have a club house key (issued by Ralph) please return it
to the Bolinas Rod & Boat Club, PO Box 248, Bolinas, CA 94924.""",

    )
# ... end of letter_bodies.


### !!!!!!!!!!!!!!!!!!!! POSTSCRIPTS !!!!!!!!!!!!!!!!! ##
post_scripts= dict(

    venmo="""
An alternative to sending a check has been provided by our
Treasurer, Angie Calpestry; details can be found here:
    https://account.venmo.com/u/bolinasrodandboatclub
""",

    angie_print="""
Please respond by either replying to this email or by post:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
""",

    remittance=""" Please send remittances to:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down on the check exactly for whom
and for what you are paying in order to prevent any confusion.""",

    ref1_email_or_PO="""[1] rodandboatclub@gmail.com or PO Box 248, 94924""",

    ref1_reservations="""[1] Reservations can be made through Anna Gade
    (uc_anna@sbcglobal.net.)""",

    covid19="""Because of the current pandemic, the Club is currently
    holding hybrid meetings, by zoom or in person. To attend in person
    you must have submitted proof of vaccination to the Club's email
    address.
    Let's hope for an early return to 'business as usual.'
    Stay safe; Stay well.""",

    forgive_duplicate="""This may be a duplication of an email
    already sent in which case please forgive.""",

    ) # end of post_scripts

authors_DOCSTRING = """   ## NOTE ##
A "Sender:" field, determined by the --mta is added to each email at
the time it is sent.  The value of the 'email' field is entered into
the 'From: ' header of the email. A "reply2" field is also available.
"""

authors = dict(  # from
    bc=dict(  # AK in British Columbia
        first="Alex",
        last="Kleider",
        suffix="",
        address="3727 Cavin Rd.",
        town="Duncan",
        state="BC",
        postal_code="V9L 6T2",
        country="Canada",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    ak=dict(  # AK in Bolinas
        first="Alex",
        last="Kleider",
        suffix="",
        address="PO Box 277",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    membership=dict(  # Membership Chair
        first="Bolinas",
        last="Rod & Boat Club",
        suffix="",
        address="PO Box 248",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nAlex Kleider (Membership)",
        email="rodandboatclub@gmail.com",
        reply2="rodandboatclub@gmail.com",
#       email="alex@kleider.ca",
#       reply2="alex@kleider.ca",
        mail_signature="\nSincerely,\n\n\nAlex Kleider (Membership)",
        ),
    )  # end of authors

content_type_docstring = """
One of the following content_types is assigned to the 'which'
attribute of an instance of utils.Club for mailing purposes.

  Each item in the following dict specifies:
      subject: re line in letter_bodies, subject line in emails
      from: expect a value from the 'authors' dict
          each value is itself a dict specifying more info...
          names, address, signatures, reply to, ..
      salutation: an optional key- if provided, it'll be used 
            instead of 'Dear First Last,'
      body: text of the letter which may or may not have
          one or more 'extra' sections.
      post_scripts:  a list of optional postscripts
      holder_funcs: assign 'working_data' attribute to holder,
            consisting of a dict keyed by personID
            and each value is a dict containing the info needed
            for each of the recipients.
      funcs: a list of functions used on each record found
            in holder.working_data and provided the data it/they
            require in that person's endry.
      test: a (usually 'lambda') function that determines
          if the record is to be considered at all.
          Probably will be redacted
      e_and_or_p: possibilities are:
          'both' email and usps,
          'email' email only,
          'usps' mail only,
       or 'one_only' email if available, otherwise usps.
  One of the following becomes the 'which' attribute
  of a Membership instance.
"""

content_types = dict(  # which_letter
    for_testing={
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["for_testing"],
        "post_scripts": (
            post_scripts['forgive_duplicate'],
            ),
        "holder_funcs": (routines.assign_just_me, ),
        "funcs": (members.std_mailing_func, ),
        "e_and_or_p": "both",
        },
    first_notice={
        "subject": "Bolinas R&B Club fees coming due",
        "from": authors["membership"],
        "body": letter_bodies["first_notice"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    June_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["June_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    July_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["July_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    statements4mailing={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["July_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "usps",
        },
    August_mailing={
        "subject": "Membership soon to expire",
        "from": authors["membership"],
        "body": letter_bodies["August_mailing"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "usps",
        },
    last_chance={
        "subject": "URGENT - LAST CHANCE TO KEEP YOUR MEMBERSHIP",
        "from": authors["membership"],
        "body": letter_bodies["last_chance"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    final_warning={
        "subject": "Membership soon to expire",
        "from": authors["membership"],
        "body": letter_bodies["final_warning"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    applicant_fee_pending={
        "subject": "BR&BC Application",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["applicant_fee_pending"],
        "post_scripts": (),
        "holder_funcs": (routines.assign_applicant_fee_pending,),
        "funcs": (members.std_mailing_func, ),
        "e_and_or_p": "one_only",
        },
    new_applicant_welcome={
        "subject": "BR&BC Application",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["new_applicant_welcome"],
        "post_scripts": (),
        "holder_funcs": (routines.assign_applicants2welcome,),
        "funcs": (members.std_mailing_func, ),
        "e_and_or_p": "one_only",
        },

    app_fee_received={
        "subject": "BR&BC Application",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["app_fee_received"],
        "post_scripts": (),
        "holder_funcs": (routines.assign_applicants2welcome,),
        "funcs": (members.std_mailing_func, ),
        "e_and_or_p": "one_only",
        },

    expired_application={
        "subject": "Application Expired",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["expired_application"],
        "post_scripts": (),
        "holder_funcs": (routines.assign_mannually, 
                        routines.add_sponsors2holder_data,),
        "funcs": (members.std_mailing_func,),
        "e_and_or_p": "one_only",
        },
    request_inductee_payment={
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["request_inductee_payment"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (routines.assign_inductees4payment,),
        "funcs": (members.inductee_payment, ),
        "e_and_or_p": "one_only",
        },

    thank={
        "subject": "Thanks for your payment",
        "from": authors["membership"],
        "cc": "",    # "cbsolution@att.net",
        "body": letter_bodies["thank"],
        "post_scripts": (),
        "holder_funcs": (),  #holder.data already assigned
        "funcs": (members.thank_func, ),
        "e_and_or_p": "one_only",
        },
#   thank={
#       "subject": "Thanks for your payment",
#       "from": authors["membership"],
#       "body": letter_bodies["thank"],
#       "post_scripts": (),
#       "holder_funcs": (, ),  # holder.data already assigned
#       "funcs": (members.thank_func,),
#       "e_and_or_p": "one_only",
#       },
    angie_print={
        "subject": "Executive Commitee Members Needed",
        "from": authors["membership"],
        "body": letter_bodies["angie_print"],
        "post_scripts": (
#           post_scripts['angie_print'],
            ),
        "funcs": [members.std_mailing_func, ],
        "test": members.is_angie,
        "e_and_or_p": "usps",
        },
    bad_address={
        "subject": "Address correction requested.",
        "from": authors["membership"],
        "body": letter_bodies["bad_address"],
        "post_scripts": (post_scripts["ref1_email_or_PO"],),
        "funcs": [members.bad_address_mailing_func, ],
        "test": members.is_member, 
        "e_and_or_p": "email",
        },
    find_enclosed={  # test will always return False!?!
        "subject": "1040-es",
        "from": authors["ak"],
        "body": letter_bodies["find_enclosed"],
        "post_scripts": (),
        "funcs": [members.std_mailing_func,],
        "test": members.is_dues_paying, 
        "e_and_or_p": "usps",
        },
    happyNY_and_0th_fees_request={
        "subject": "Happy New Year from the Bolinas R&B Club",
        "from": authors["membership"],
        "body": letter_bodies["happyNY_and_0th_fees_request"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (
                  members.std_mailing_func),
        "test": members.is_dues_paying,
        "e_and_or_p": "one_only",
        },
    feb_meeting={
        "subject": "Meeting first Friday of February",
        "from": authors["membership"],
        "body": letter_bodies["feb_meeting"],
        "post_scripts": (
            post_scripts['ref1_reservations'],
            ),
        "funcs": (members.std_mailing_func,),
#       "test": members.is_dues_paying, 
        "e_and_or_p": "email",
        },
    correction={
        "subject": "Corrected fees statement",
        "from": authors["membership"],
        "body": letter_bodies["correction"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (
                  members.std_mailing_func),
        "test": lambda record: True if (
            members.is_dues_paying(record) and
            members.not_paid_up(record)
            ) else False,
        "e_and_or_p": "one_only",
        },
    interim_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["interim_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    bad_email={
        "subject": "non-working email",
        "from": authors["membership"],
        "body": letter_bodies["bad_email"],
        "post_scripts": (),
        "funcs": (members.std_mailing_func,),
        "test": (lambda record: True if
                 'be' in record["status"].split(members.SEPARATOR)
                 else False),
        "e_and_or_p": "usps",
        },
    waiting4application_fee={
        "subject": "Application Received",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["waiting4application_fee"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    awaiting_vacancy={
        "subject": "Membership pending vacancy",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["awaiting_vacancy"],
        "post_scripts": (),
        "funcs": (members.std_mailing_func,),
        "test": (lambda record: True if members.is_inductee(record)
                                 else False),
        "e_and_or_p": "one_only",
        },
    vacancy_open={
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["vacancy_open"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    second_request_inductee_payment={
        "subject": "Still awaiting Club dues",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies[
            "second_request_inductee_payment"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            post_scripts['venmo'],
            ),
        "holder_funcs": (club.set_include0_false,
                         routines.assign_owing, ),
        "funcs": (members.send_statement, ),
        "e_and_or_p": "one_only",
        },
    welcome2full_membership={
        # will probably be redacted in favour of
        # first_dues_payment_welcome
        "subject": "You are a member!",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["welcome2full_membership"],
        "post_scripts": (post_scripts["ref1_email_or_PO"],
                         ),
        "holder_funcs": (routines.assign_welcome2full_membership,),
        "funcs": (members.q_mailing,),
        "e_and_or_p": "one_only",
        },

    first_dues_payment_welcome={
        # called by code/ap_update.appD
        "subject": "You are a member!",
        "from": authors["membership"],
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": letter_bodies["first_dues_payment_welcome"],
        "post_scripts": (),
        "holder_funcs": (),
        "funcs": (members.q_mailing,),
        "e_and_or_p": "one_only",
        },

    retirement_from_club={
        "subject": "Sorry you're leaving us.",
        "from": authors["membership"],
        "body": letter_bodies["retirement_from_club"],
        "post_scripts": (),
        "funcs": (members.std_mailing_func,),
        "test": (lambda record: True),
        "e_and_or_p": "one_only",
        },

    membership_termination={ # Incl stamped self addressed envelope)
        "subject": "Sorry you're leaving us.",
        "from": authors["membership"],
        "body": letter_bodies["membership_termination"],
        "post_scripts": (),
        "funcs": (members.std_mailing_func,),
        "test": (lambda record: True if members.is_terminated(record)
                 else False),
        "e_and_or_p": "usps",
        },

    )
# ... end of content_types.
ctypes = sorted([key for key in content_types.keys()])

printers = dict(
    # tuples in the case of envelope windows.
    # Smaller envelope.  #9: 3-7/8 x 8-7/8"
    HL8260W_e10=dict(  # large envelopes, Bolinas Data Closet
        indent=4,
        top=4,  # blank lines at top
        frm=(4, 35),  # return window
        date=5,  # between windows
        to=(5, 29),  # recipient window
        re=4,  # below windows => fold
        ), # 3+4+5+5+4 = 21
    HL2170_e10=dict(  # large envelopes, Cavin Rd usb printer
        indent=3,
        top=1,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    peter_e10=dict(  # Larger envelope. #10: 4-1/8 x 9-1/2"
        indent=5,
        top=4,  # blank lines at top
        frm=(4, 25),  # return window
        date=5,  # between windows
        to=(6, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    angie_e9=dict(    # Smaller envelope.  #9: 3-7/8 x 8-7/8"
        indent=0,
        top=0,  # blank lines at top
        frm=(4, 40),  # return window
        date=7,  # between windows
        to=(7, 40),  # recipient window
        re=3,  # below windows => fold
        ),
   )
# ## ... end of printers (dict specifying printer being used.)

def assign_printer(holder):
    """
    """
    # there's a bug here that hasn't been resolved
    # inline code used in code.command.prepare_mailing
    # rather than this function
    _ = input("Ready to go ahead with assign_printer?")
    print("Entering assign_printer")
    _ = input("Should see Entering ... on line above!")
    menu = routines.get_menu_dict(printers.keys())
    print("Printer to use...")
    for key, lpr in menu.items():
        print(f"{key}: {lpr}")
    index = int(input("Which printer will you be using: "))
    holder.printer = menu[index]

def get_postscripts(which_letter):
    """
    Returns a list of lines representing the post scripts
    """
    ret = []
    n = 0
    for post_script in which_letter["post_scripts"]:
        ret.append("\n" + "P"*n + "PS " + post_script)
        n += 1
    return ret


def prepare_letter_template(which_letter, lpr):
    """
    Prepares the template for a letter.
    <which_letter>: one of the <content_types> and
    <printer>: one of the keys to the <printers> dict
    Returns a 'letter' /w formatting fields.
    """
    ret = [""] * lpr["top"]  # add blank lines at top
    # return address:
    ret_addr = address_format.format(**which_letter["from"])
    ret.append(helpers.expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(helpers.expand(
            (helpers.get_datestamp()), lpr['date']))
    # format string for recipient adress:
    ret.append(helpers.expand(address_format, lpr['to'][0]))
    # subject/Re: line
    ret.append(helpers.expand(
        "Re: {}".format(which_letter["subject"]), lpr['re']))
    # format string for salutation:
    try:
        ret.append(which_letter["salutation"] + "\n")
    except KeyError:
        ret.append("Dear {first} {last}{suffix},\n")
    # body of letter (with or without {extra}(s))
    ret.append(which_letter["body"])
    # signarue:
    ret.append(which_letter["from"]["mail_signature"])
    # post script:
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)


def prepare_email_template(which_letter):
    """
    Prepares the template for an email.
    Used by utils.prepare_mailing_cmd,
    Format fields are subsequently filled by **record.
    """
    ret = ["Dear {first} {last}{suffix},"]
    ret.append(which_letter["body"])
    ret.append(which_letter["from"]["email_signature"])
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)


def assign_templates(holder):
    # assign_templates(holder) moved from commands to content!
    ret = ["Assigning printer & templates...",
           "within code.content.assign_templates",]
    menu = helpers.get_menu_dict(printers.keys())
    print("Printer to use...")
    for key, lpr in menu.items():
        print(f"{key}: {lpr}")
    index = int(input("Which printer to use? "))
    lpr = menu[index]
    ret.append(
        f"          for 'printer'.. {index:>3}: {lpr}")
    holder.lpr = printers[lpr]
    holder.letter_template = prepare_letter_template(
            holder.which,
            holder.lpr)
    holder.email_template = prepare_email_template(
            holder.which)
    return ret

def contents():
    """
    Provides a way of getting a quick glimpse
    of the various contents provided.
    Typical usage:
        print('\n'.join(contents()))
    """
    tuples = (('custom_lambdas', custom_lambdas),
              ('letter_bodies', letter_bodies),
              ('post_scripts', post_scripts),
              ('authors', authors),
              ('content_types', content_types),
              ('printers', printers),
              )
    ret = []
    for tup in tuples:
        ret.append('')
        ret.append(tup[0])
        ret.append('=' * len(tup[0]))
        r = []
        for key in tup[1]:
            r.append(key)
        ret.extend(helpers.tabulate(r,
                                    alignment='<',
                                    max_width=140,
                                    separator=' | ')
                   )
    return ret


def main():
    print("content.py has no syntax errors")
    which = content_types["for_testing"]
    lpr = printers["HL8260W_e10"]
    letter = prepare_letter_template(which, lpr)
    email = prepare_email_template(which)
    rec = dict(
        first="Jane",
        last="Doe",
        suffix=" Jr",
        address="nnn An Ave.",
        town="Any Town",
        postal_code="CODE",
        state="CA",
        country="USA",
        email="myemail@provider.com",
        extra="""A lot more junk:
Certainly nothing very serious!
Just a lot of junk.""",
        )
    print("Letter follows...")
    print(letter.format(**rec))
    with open("letter2print", 'w') as fout:
        fout.write(helpers.indent(letter.format(**rec),
                                  lpr['indent']))
    print("Email follows...")
    print(email.format(**rec))
    with open("email2print", 'w') as fout:
        fout.write(email.format(**rec))


duplicate_email_template = """From: rodandboatclub@gmail.com
To: {}
Subject: Which email is best?

Dear {},
Club records have two differing emails for you:
    "{}" and
    "{}" .
Please reply telling us which is the one you want the club to use.
Thanks in advance,
Membership"""



if __name__ == "__main__":
#   def ck_assign_printer():
#       class Holder(object):
#           def __init__(self):
#               noval = ''
#       holder = Holder()
#       assign_printer(holder)
#       print(holder.printer)
#       print(printers[holder.printer])

#   ck_assign_printer()
    main()
#   print('\n'.join(contents()))
#   print("content.py compiles OK")
else:
    pass
#   def print(*args, **kwargs):
#       pass



