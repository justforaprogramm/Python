"""re.sub(pattern, repl, string, count=0,flags=0)
   re.findall(pattern, string, flags=0)
"""

import re

url = input("URL: ").strip()

if matches:= re.search(r"^(?:https?://)?(?:www\.)?twitter\.(.+)/([a-z0-9_]+)$", url, re.IGNORECASE):
    if  matches.group(1) == "com":
        print(f"Username:", matches.group(2))