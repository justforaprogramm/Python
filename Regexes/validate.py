"""docs.python.org/3/library/re.html
   re.search(pattern, string, flags=0)
   "." any character except a newline
   "*" 0 or more repetitions
   "+" 1 more repetition
   "?" 0 or 1 repetition
   "{m}" m repetitions
   "{m, n}" m to n repetitions
   
   ^ matches start of string
   $ matches end of string before newline
   [] set of characters
   [^] complementing the set
   
   \d decimal digit
   \s whitespace characters
   \w word character ... as well as numbers and the underscore
   uppercase = opposite
   
   A|B either A or B
   (...) a group
   (?:...) non-capturing version
   
   r regular expresion
"""
import re
email = input("What's your email? ").strip()

if re.search(r"^(\w|\.)+@(\w+\.)?\w+\.com$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid") 