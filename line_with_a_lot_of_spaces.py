# When you do not specify a delimiter, multiple spaces are treated like one delimiter

# example 1
# line = ' A lot           of spaces'
# etc = line.split()
# print(etc)

# example 2
line = 'first;second;third'
# thing = line.split()
# print(thing)
# print(len(thing))

# example 3
# example 3 requires that you uncomment line variable in example 2
thing = line.split(';')
print(thing)
print(len(thing))
