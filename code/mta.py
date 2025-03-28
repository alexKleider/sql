#!/usr/bin/env python

# File: mta.py      ("--mta" command line option.)
# used to be called "config.py" which conflicts
# with the Python standard library
# within Sql code base this is being moved onto the send_email
# function rather than being imported. 

"""
Provides infrastructure for send_emails.py in
the SQL code base and for send.py elsewhere.

Three hard links:
this file is used by the following code bases:
    1. the ~/Git/Club/Utils: mta.py (used to be: Pymail/config.py)
    2. the ~/Git/Lib: code/config.py
    2. the ~/Git/Sql: code/Pymail/config.py

SSL (Secure Sockets Layer) is deprecated in favour of
TLS (Transport Layer Security)
"""

import sys
import os

def getpw(service):
    """
    Passwords are in highly restricted dot files.
    Each file contains only the password.
    """
    with open(
        os.path.expanduser('~/.pw.{}'.format(service)), 'r') as f_obj:
        return f_obj.read().strip()


# mta = dict(
config = dict(
    sonic= {
        "host": "smtp://akleider@mail.sonic.net",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "akleider@sonic.net",
        "from": "akleider@sonic.net",
        "password": getpw("sonic"),
        "tls": "on",
    },
    easy= {
        "host": "mailout.easydns.com",
        "tls_port": "587",
        "ssl_port": "465",  # SSL deprecated predecessor to TLS
#       "port": "2025",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
        "from": "alex@kleider.ca",
        "password": getpw("easy"),
        "tls": "on",
    },
# google no longer provides smtp services so 
# the following two won't work!!
    akg= {
        "host": "smtp.gmail.com",
        "port": "587",
        "tls_port": "587",
        "port": "587",
        "ssl_port": "465",
        "user": "alexkleider@gmail.com",
        "from": "alexkleider@gmail.com",
        "password": getpw("akg"),

    },
    clubg= {
        "host": "smtp.gmail.com",
        "port": "587",
        "tls_port": "587",
        "ssl_port": "465",
        "user": "rodandboatclub@gmail.com",
        "from": "rodandboatclub@gmail.com",
        "password": getpw("clubg"),

    },
)

if __name__ == '__main__':

    print("Passwords are redacted for security reasons!!")
    sys.exit()

    ### For testing only: comment out above two lines.
    pws = set()
    for key in config:
        pws.add(config[key]["password"])
    print("Passwords are:")
    print(repr(pws))

