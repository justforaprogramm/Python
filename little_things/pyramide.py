j = 7
for i in range(1, j+1, 2):
    print(' ' * (j-(i//2)) ,'*' * i, sep='')

for i in reversed(range(1, j+1, 2)):
    print(' ' * (j-(i//2)) ,'*' * i, sep='')