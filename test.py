
first = 'Alex'
last = 'Kleider'
params = [name+'%' if name else name for name in (first, last,)]
print(params)

first = 'Alex'
last = ''
params = [name+'%' if name else name for name in (first, last,)]
print(params)
