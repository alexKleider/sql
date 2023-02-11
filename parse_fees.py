#!/usr/bin/env python3

# File: parse_fees.py

dock_f = 'Secret/dock_list.txt'
kayak_f = 'Secret/kayak_list.txt'
mooring_f = 'Secret/mooring_list.txt'


with open(dock_f, 'r') as inf:
    """
    personID TEXT NOT NULL UNIQUE,
    --no one will pay for >1 
    --so no need for an
    --auto generated PRIMARY KEY
    cost NUMERIC DEFAULT 75
    """
    for line in inf:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        first_last, fee = line.split(':')
        fee = int(fee)
        first, last = first_last.split()
        print(f"{first} {last}: {fee}")

with open(kayak_f, 'r') as inf:
    """
    slotID INTEGER PRIMARY KEY,
    personID TEXT,  --foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 kayak slot.
    slot_code TEXT NOT NULL UNIQUE,
    slot_cost NUMERIC DEFAULT 70
    """
    for line in inf:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        code_name, fee = line.split(':')
        fee = int(fee)
        code, first, last = code_name.split()
        print(f"{code} {first} {last}: {fee}")

with open(mooring_f, 'r') as inf:
    """
    mooringID INTEGER PRIMARY KEY,
    personID TEXT, --foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 mooring.
    mooring_code TEXT NOT NULL UNIQUE,
    mooring_cost NUMERIC DEFAULT 0
    """
    for line in inf:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.rfind('#') > -1:
            line = line.split('#')[0].strip()
#       _ = input(f"usable line: {line}")
        parts = line.split()
        l = len(parts)
        if l == 1:
            code = parts[0]
            fee, first, last = '0', '', ''
        elif l == 2:
            code, fee = parts
            first, last = '', ''
        elif l == 4: 
            code, fee, first, last = parts
        else:
            _ = input(f"parts ({l}): {parts}")
        fee = int(fee)
        print(f":'{code}' '{fee}'  '{first}' '{last}'")

