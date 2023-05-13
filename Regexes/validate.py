"""docs.python.org/3/library/re.html
   re.search(pattern, string, flags=0)
"""
import re
email = input("What's your email? ").strip()

if re.search("@", email):
    print("Valid")
else:
    print("Invalid")