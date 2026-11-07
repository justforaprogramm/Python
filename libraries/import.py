"""
docs.python.org/3/library/random.html
docs.python.org/3/library/statistics.html
pypi.org/project/cowsay
pypi.org/project/requests
pypi.org

import 
random.coice(seq)
from
"""
#from random import choice

#coin = choice(["heads", "tails"])
#print(coin)

#       random      #
import random

coin = random.choice(["heads", "tails"])
print(coin)

number = random.randint(1,10)
print(number, end="\n\n")

cards = ["jack", "queen", "king"]
random.shuffle(cards)
for card in cards:
    print(card)

import statistics

print(statistics.mean([100, 90]))

#       sys        #
import sys

if len(sys.argv) < 4:
    sys.exit("Too few arguments, two needet")
elif len(sys.argv) > 4:
    sys.exit("Too many arguments, only two needet")

for arg in sys.argv[1:]:
    print("hello, myy name is", arg)
    
    
#       cowsay      #
import cowsay

if len(sys.argv) == 4:
    cowsay.trex("hello, " + sys.argv[1])