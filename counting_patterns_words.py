# The general pattern to count the words in a line of text is to split the line into words
# Then loop through the words and use a dictionary to track the count of each word independently.
counts = dict()
print('Enter a line of text:')
line = input('')

words = line.split()

print('Words:', words)
print('Counting...')
for word in words:
    counts[word] = counts.get(word, 0) + 1
print('Counts', counts)
