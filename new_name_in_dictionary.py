# When we encounter a new name, we need to add a new entry in the dictionary
# If this is the second or later time that we have seen the name, we simply add one to the count in the dictionary under that name
counts = dict()
names = ['csev', 'cwen', 'csev', 'zgian', 'cwen']
for name in names:
    if name not in counts:
        counts[name] = 1
    else:
        counts[name] = counts[name] + 1
print(counts)
