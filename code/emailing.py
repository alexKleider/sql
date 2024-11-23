#!/usr/bin/env python3

# File code/emailing.py

"""
Provides email related functionality:
    display_cmd   &
    send_cmd
...both use the default input (json) and 
in the case of display there is also a default output file.
When executed directly can accept command line args as follows:
args: "-i", "--input_file", "-o", "--output_file"

"""
import sys

try: from code.club  import EMAIL_JSON as json_email_file
except ImportError: from club import EMAIL_JSON as json_email_file
#except ImportError: json_email_file = 'Secret/emails.json'

try: from code import helpers
except ImportError: import helpers

try: from code import mta
except ImportError: import mta

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
import hashlib
import time
import random
import argparse
parser = argparse.ArgumentParser()

readable_email_file = "emails.txt"
parser.add_argument("-i", "--input_file",
                help="specify non default value for input file",
                default=json_email_file)
parser.add_argument("-o", "--output_file",
                help="specify non default value for output file",
                default=readable_email_file)
args = parser.parse_args()

wait = True   # creates a 1-5 second delay between emails
    # could probably set to False since no longer using gmail

MIN_PAUSE = 1   #} Seconds between
MAX_PAUSE = 5   #} email postings.

def update_kwargs(**kwargs):
    print(
    "For each value: Rtn to accept default or enter new value.")
    ret = {}
    while True:
        for key, value in kwargs.items():
            new_val = input(
                    f"<{key}> defaults to '{value}': ")
            if new_val:
                if new_val in  {"''", '""'}:
                    new_val = ""
                ret[key] = new_val
            else: ret[key] = kwargs[key]
        print("OK with the following values?...")
        for key, value in ret.items():
            print(f"  {key}: {value}")
        yn = input("Accept above values? (y/n) ")
        if yn and yn[0] in "yY":
            break
    return ret

def update_dict(default_dict):
    print(
    "For each value: Rtn to accept default or enter new value.")
    ret = {}
    while True:
        for key, value in default_dict.items():
            new_val = input(
                    f"<{key}> defaults to '{value}': ")
            if new_val:
                if new_val in  {"''", '""'}:
                    new_val = ""
                ret[key] = new_val
            else: ret[key] = default_dict[key]
        print("OK with the following values?...")
        for key, value in ret.items():
            print(f"  {key}: {value}")
        yn = input("Accept above values? (y/n) ")
        if yn and yn[0] in "yY":
            break
    return ret

def pause():
    """
    Provides a random interval between emails so that the
    MTA is less likely to think the process is automated.
    Implemented when gmail was used so is probably no longer
    necessary.
    """
    time.sleep(random.randint(MIN_PAUSE,
                              MAX_PAUSE))


def into_string(header_value):
    """
    Returns a string (possibly empty.)
    If given a list it must be of strings and a comma/space
    separated concatination is returned.
    """
#   print("<header_value> '{}' is of type {}."
#       .format(header_value, type(header_value)))
    if isinstance(header_value, str):
        return header_value
    elif isinstance(header_value, list):
        return ', '.join(header_value)
    else:
        return ''


def attach(attachment, msg):
    """
    <msg>: an instance of MIMEMultipart() to which to add
    the attachment.
    <attachment> is the name of a file to become an attachment.
    This code has been successfully tested to work for the
    following types of files: text, .docx, .pdf, ..
    so is expected to work for all files.
    """
    basename = os.path.basename(attachment)
    with open(attachment, "rb") as f_obj:
        part = MIMEApplication(
            f_obj.read(), basename)
    # After the file is closed
    part['Content-Disposition'] = (
        'attachment; filename="%s"' % basename)
    msg.attach(part)


def attach_many(attachments, msg):
    """
    This code was 'plagerized' from the web.
    It is a slightly modified version of an excerpt of
    code submitted by vijay.anand found here..
    https://stackoverflow.com/questions/52292971/sending-single-email-with-3-different-attachments-python-3
    It is failing and therefore not used.  It's being left here
    in the hopes that it can be mended.
    """
    for attachment in attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        maintype, subtype = content_type.split("/", 1)
        if maintype == "text":
            with open(attachment) as fp:
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == "image":
            with open(attachment, "rb") as fp:
                attachment = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == "audio":
            with open(attachment, "rb")as fp:
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(attachment, "rb") as fp:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment",
                            filename=os.path.basename(attachment))
        msg.attach(attachment)

def readable_emails(json_email_file=json_email_file, report=None):
    """
    Reads the json file and returns human readable text.
    """
    records = helpers.get_json(json_email_file, report=report)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
            email.append("{}: {}".format(field, record[field]))
        email.append('')  # a line separator
        all_emails.extend(email)
        n_emails += 1
    helpers.add2report(report,
        f"Processed {n_emails} emails...", also_print=True)
    return "\n".join(all_emails[:-1])  # lose teminal blank line

def display_cmd(report=None):
    with open(readable_email_file) as out_f:
        out_f.write(readable_emails( # default json file name
            report=report))
    helpers.add2report(report, 
        ["Sent human readable version of emails to ",
        f"{readable_email_file}"],
        also_print=True)

def send_emails(email_json=json_email_file, report=None):
    """
    Sends emails prepared by prepare_mailing_cmd.
    """
#   if confirm:  # not using curses: check 'lesssecureapps' setting.
#       ck_lesssecureapps_setting()
    helpers.add2report(report,
            "Setting up mta within code/emailing.send_emails...",
            also_print=True)
    agent = "easy"
    emailer = "python"
    if emailer == "python":
        send_func = Pymail.send.send
        helpers.add2report(report,
            f"Using Python modules to dispatch emails.",
            also_print=True)
    elif emailer == "bash":  # will probably redact this
        send_func = Bashmail.send.send
        helpers.add2report(report,
            f"Using Bash to dispatch emails.",
            also_print=True)
    else:
        helpers.add2report(report,
            [f'"{emailer}" is an unrecognized "--emailer" option.',
            "Aborting execution!"],
            also_print=True)
        sys.exit(1)
    message = None
    data = helpers.get_json(email_json, report=report)
    Bashmail.send.send(data, agent, include_wait=wait)


def send(emails, agent='easy', report=None,
                            include_wait=True):
    """
    Sends emails using Python modules.
    <emails> is a list of dicts (typically collected from a json
    file.) Each dict represents an email to be sent and can have
    the following keys, some optional:
    'body': a (possibly empty) string.
    'attachments': a list (possible empty) of file names.
    'From', 'Reply-To', 'To', 'Subject', ...
    and possibly other commonly used fields defined by rfc5322.
    Values are either strings or lists of strings in which case
    the values are converted into a single comma separated string.
    <include_wait> if True inserts a pause after each mailing.
    """
    n_emails = len(emails)
    counter = 0
#   print("Using {} as MTA...".format(agent))
    server = mta.config[agent]
    sender = server["from"]
    helpers.add2report(report,
        "Initiating SMTP: {host} {port}".format(**server),
        also_print=True)
    s = smtplib.SMTP(host=server['host'], port=server['port'])
    s.starttls()
    s.ehlo
    # Comment out one of the following two:
#   testing = True     # Very INSECURE: use only for testing.
    testing = False    # This should be the default.
    s.login(server['user'], server['password'])
    helpers.add2report(report,
        f"Successfully connected to {agent}", also_print=True)
    response = input("... Continue? ")
    if not (response and response[0] in 'yY'):
        sys.exit()
    try:
        for email in emails:
            email["Sender"] = sender
            msg = MIMEMultipart()
            body = email['body']
            attachments = email['attachments']
            del email['body']
            del email['attachments']
            counter += 1
            helpers.add2report(report,
                f"Sending email {counter} of {n_emails} ...",
                also_print=True)
            for key in email:
                print(f"\t{key}: {email[key]}")
                msg[key] = into_string(email[key])
            msg.attach(MIMEText(body, 'plain'))
#           attach_many(attachments, msg) ## Fails, 2b trouble sh.
            for attachment in attachments:
                attach(attachment, msg)
            try:
                s.send_message(msg)
            except SMTPDataError:
                helpers.add2report(report,
                    "FAILURE sending email " +
                    f"#{n} to {email['To']}",
                    also_print=True)
                continue
            if include_wait:
                pause()
    except:
        s.quit()
        helpers.add2report(report,
            "Pymail.send.send() failed sending to {}."
                .format(email['To']), also_print=True)
        raise
    s.quit()


def send_cmd(report=None):
    send_emails(email_json=json_email_file, report=report)



def emails_cmd(report):
    """
    Provides choice: to inspect or send emails.
    Essentially choose between "Inspect" which reads the email
    json file and sends a human readable version to emails.txt
    and "Send" which sends the emails found in the json file.
    """
    helpers.add2report(report,
            "Preparing to display or send emails.",
            also_print=True)

    while True:
        report.append(
                "Choose to I)nspect or S)send emails: ")
        choice = input(report[-1])
        if choice:
            if choice[0] in 'iI':
                out_f = input(
                    f"Accept default ({readable_email_file})"
                    + "or enter new name: ")
                if not out_f: out_f = readable_email_file 
                report.append(
                        f"...sending emails to {out_f}...")
                with open(out_f, 'w') as stream:
                    stream.write(readable_emails(
                        json_email_file))   # DISPLAY emails
                break
            elif choice[0] in 'sS':
                helpers.add2report(report,
                    "Sending emails...", also_print=True)
                send(helpers.get_json(json_email_file),
                        report=report)   # SEND emails
                helpers.add2report(report,
                    "...emails send.", also_print=True)
                break
            else:
                report.append("Invalid choice!")
                print(report[-1])
        else:
            helpers.add2report(report,
            "Empty response ==> termination.", also_print=True)
            print(report[-1])
            break

def main():
    report = ["Runnning code/emailing.py",]
    json_email_file = args.input_file
    helpers.add2report(report,
        [f"json email file set to {args.input_file}",
         f"output txt file set to {args.output_file}"],
        also_print=True)
    yn = input("OK to procede? (y/n) ")
    if not (yn and yn[0] in "yY"):
        helpers.add2report(report,
            "Aborting execution.", also_print=True)
        sys.exit()
    emails_cmd(report)
    print("A report follows....")
    for line in report:
        print(line)


def ck_defaults():
    defaults = dict(
            first="Alex",
            middle="NMI",
            last="Kleider",
            )
    print("Going in...")
    for key, value in defaults.items():
        print(f"  {key}: {value}")

    print("Using update_dict...")
    for key, value in update_dict(defaults).items():
        print(f"  {key}: {value}")

    print("Using update_kwargs...")
    for key, value in update_kwargs(**defaults).items():
        print(f"  {key}: {value}")



if __name__ == "__main__":
    ck_defaults()

