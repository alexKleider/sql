#!/usr/bin/env python3

# File: integer.py

def get_int(prompt, n=0):
    """
    Returns a non negative integer of users choice.
    If n is provided, it is the highest number possible.
    """
    while True:
        value = input(prompt)
        try:
            value = int(value)
#           break
        except ValueError:
            print("Must enter an integer!")
            continue
        if n and value>n:
            print("Must be 0 ... {n}")
            continue
        elif value < 0:
            print("Must not be negative.")
            continue
        else: return value
    return value

if __name__ == "__main__":
    n = get_int("Give me an int < 7: ", n=7)
    print(n)

