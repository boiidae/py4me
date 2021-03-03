# Example of a nested decision
# A one-branch if statement showing an if statement within an if statement
# Try it with numbers below and above 100 to see the different results
x=42
if x > 1:
    print('More than one')
    if x < 100:
        print('Less than 100')
print('all done')
