#!/usr/bin/env python3

# File code/send_emails_in_code.py

from Pymail import send

try: from code import club
except ImportError: import club

try: from code import helpers
except ImportError: import helpers

try: from code import Pymail
except ImportError: import Pymail

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


def main(report):
    while True:
        report = [
            "Choose to I)nspect or S)send emails: ", ]
        choice = input(report[0])
        if choice:
            holder = club.Holder()
            if choice[0] in 'iI':
                outfile = input(
                        "Send emails to which text file: ")
                report.append(
                        f"...sending emails to {outfile}...")
                with open(outfile, 'w') as stream:
                    stream.write(display_emails_cmd(holder))
                break
            elif choice[0] in 'sS':
                report.append("Sending emails...")
                print(report[-1])
                send_emails(holder)
                report.append("...emails send.")
                print(report[-1])
                break
            else:
                report.append("Invalid choice!")
                print(report[-1])
        else:
            report.append("Empty response ==> termination.")
            print(report[-1])
            break


if __name__ == "__main__":
    main()

