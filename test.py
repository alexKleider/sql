from code import dates

while True:
    personID = int(input("personID to query: "))
    if personID <= 0: break 
    print(f"{repr(dates.get_demographic_dict(personID))}")
