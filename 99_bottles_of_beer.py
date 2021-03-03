# 99 Bottles of Beer on the wall example
beer = input('How many bottles of beer on the wall? ')
wall = int(beer)
while wall > 0:
    print(wall, 'bottles of beer on the wall,', wall, 'bottles of beer of beer')
    print('take one down, pass it around, now you have')
    wall = wall - 1
    print( wall,'bottles of beer on the wall')
    print()
print('hic... oh no! no more beer!')
