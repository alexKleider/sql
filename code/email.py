#!/usr/bin/env python3

# File code/email.py

try: from code import club
except ImportError: import club

try: from code import helpers
except ImportError: import helpers

try: from code import Pymail
except ImportError: import Pymail
from Pymail import send

def display_emails_cmd(holder):
    records = helpers.get_json(holder.email_json, report=True)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)


def send_emails(holder):
    """
    Sends emails prepared by prepare_mailing_cmd.
    """
    # gmail no longer provides smtp services so next 2 lines redacted
#   if confirm:  # not using curses: check 'lesssecureapps' setting.
#       ck_lesssecureapps_setting()
    mta = "easy"
    emailer = "python"
    if emailer == "python":
        send_func = Pymail.send.send
        print("Using Python modules to dispatch emails.")
    elif emailer == "bash":  # will probably redact this
        send_func = Bashmail.send.send
        print("Using Bash to dispatch emails.")
    else:
        print('"{}" is an unrecognized "--emailer" option.'
              .format(emailer))
        sys.exit(1)
    wait = mta.endswith('g')
    message = None
    data = helpers.get_json(holder.email_json, report=True)
    send_func(data, mta, include_wait=wait)



if __name__ == "__main__":
    choice = input("Choose to I)nspect or S)send emails ('i' or 's'):")
    if choice:
        holder = club.Holder()
        if choice[0] in 'iI':
            outfile = input("Send emails to which text file: ")
            with open(outfile, 'w') as stream:
                stream.write(display_emails_cmd(holder))
        elif choice[0] in 'sS':
            send_emails(holder)
        else:
            print("Invalid choice.")
