#!/usr/bin/env python3

# File: pmc  (rewrite of prepare_mailing_cmd)

import os
from code import club
from code import helpers
from code import content

"""
Rewrite of prepare_mailing_cmd

Would like to delay specifying a printer until we know there's
a need to print (ie usps mailings as well as emails.)
"""

def pmc(report=None):
    """
    **prepare_mailing_cmd under revision**
    ck for 'cc', especially in response to 'sponsors'
    & assign holder.cc if needed
    insert checks regarding mail dir and email.json
    then set up mailing dir and holder.emails (a
                             list of dicts for emails)
    Traverse records applying funcs
      populating holder.mail_dir and holder.email list
    Move holder.email listing into a json file (if not empty.)
    Delete mail_dir if it's empty
    """
    holder = club.Holder()  # Club related globals
    ret = []
    # give user opportunity to abort if files are still present:
    print("Checking for left over files (must be deleted!) ...")
    helpers.check_before_deletion((holder.email_json,
                                    holder.mail_dir),
                                    delete=True)
    os.mkdir(holder.mail_dir)
    # choose letter type and assign to holder.which
    response = helpers.get_menu_response(content.ctypes)
    if response == 0:
        ret.append("Quiting per your choice")
        helpers.add2report(report, ret, also_print=True)
        return ret
    w_key = content.ctypes[response-1]  # which_key
    ret = [
        f"Your choice for 'w_key'.. {response:>3}: {w_key}", ]
    _ = input(ret[0])
    holder.which = content.content_types[w_key]
    # which letter has been established & conveyed to the holder
    # now: establish printer to be used and assign templates
#   _ = input(holder.which.keys())
    if {"cc", "bcc"} and set([key for key in holder.which.keys()]):
        holder.cc_sponsors = True
    ret.extend(content.assign_templates(holder)) #sets printer
    # cc and bcc (incl sponsors) should be done in q_mailing
    # prepare holder for emails
    holder.emails = []
    # collect data..
    for func in holder.which['holder_funcs']:
#       _ = input(f"running holder func {repr(func)}.")
        # assigns holder.working_data (found in routines:
        #   (routines.assign_applicants2welcome,),
        #   (routines.assign_welcome2full_membership,),
        func(holder)
    for dic in holder.working_data.values():
        for func in holder.which['funcs']:  #  vvvvv
#           _ = input(f"Running func {repr(func)}")
            # for billing: members.send_statement(holder, dic)
            # otherwise: members.q_mailing
#           ret.extend(func(holder, dic))
            func(holder, dic)
    # send holder.emails to a json file
    # Would like to add option of appending to existing json
    #  ie provide option of using code.helpers.add2json_file()
    if holder.emails:
        helpers.dump2json_file(holder.emails,
                holder.email_json)
        n = len(holder.emails)
        efile = holder.email_json
        print(f"{n} emails sent to {efile}.")
        print(f"Emails ({len(holder.emails)} in " +
            f"number) sent to {holder.email_json}")
    else:
        print("No emails to send.")
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
    helpers.add2report(report, ret, also_print=False)
    print("prepare_mailing completed..")
    return ret


if __name__ == "__main__":
    pmc()
