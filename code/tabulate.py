#!/usr/bin/env python3

# File: tabulate.py

"""
Provides a listing of member & applicant names in last, first
format tabulated for printing in landscape mode.
"""

import commands
path2insert = '/home/alex/Git/Club/Utils'
# the above code can be found @
# https://github.com/alexKleider/Club_Utilities
import os
import sys
sys.path.insert(0, path2insert)
import helpers

ret = helpers.tabulate(commands.for_angie(include_blanks=False),
        max_width=133, separator='  ')
print('\n'.join([item for item in ret if item]))
