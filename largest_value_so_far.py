largest_value_so_far=-1
print('Before', largest_value_so_far)
for the_num in [9, 41, 12, 3, 74, 15]:
    if the_num>largest_value_so_far:
        largest_value_so_far=the_num
    print(largest_value_so_far, the_num)

print('After', largest_value_so_far)
