"""
docs.python.org/3/libary/functions.html

Str = String
int = Integer

print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

.title() = Uppercase all letters after Space
.capitalize() = Uppercase the first letters after Space
""" 

# Ask User For name and save value + Remove blank
name = input("What's your name? ").strip().title()

#Split input
first, last = name.split(" ")

# Say hello to user with saved value "name"
# print("Hello," , name + "!")
# print('hello, ', name, sep='!', end='LOL\n')
print(f'hello, {first}', end='!\n')