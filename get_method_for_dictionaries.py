# The pattern of checking to see if a key is already in a dictionary
# and assuming a default value if the key is not there is very common
# It is so common that there is a method called get() that does this for us
# Default value if key does not exist (and no Traceback).
counts = dict()
names = ['csev', 'cwen', 'csev', 'zgian', 'cwen']
for name in names:
    counts[name] = counts.get(name, 0) + 1
print(counts)
