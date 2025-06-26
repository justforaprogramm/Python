line_between = 1
max_witdh = 10
for i in range(1, max_witdh+1, 2):
    print(' ' * (max_witdh-(i//2)) ,'*' * i, sep='', end=('\n'*line_between if line_between > 0 else '\n'))

for i in reversed(range(1, max_witdh+1, 2)):
    print(' ' * (max_witdh-(i//2)) ,'*' * i, sep='', end=('\n'*line_between if line_between > 0 else '\n'))