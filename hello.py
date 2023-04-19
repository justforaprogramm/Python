"""
docs.python.org/3/libary/functions.html

print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
Str = String

""" 

#Ask User For name and save value
name = input("What's your name? ")
#Say hello to user with saved value "name"
print("Hello," , name + "!")
#example
print('hello, ', name, sep='!', end='LOL\n')
print(f'hello, {name}', end='!\n')