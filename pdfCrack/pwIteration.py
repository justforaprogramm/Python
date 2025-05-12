from itertools import product
import string
from os import path

# Ordnerpfad, in dem das Script liegt
fpath = path.dirname(path.abspath(__file__))

# Zeichensatz: Zahlen, Buchstaben, Sonderzeichen und Leerzeichen
charset = string.digits + string.ascii_letters + string.punctuation + ' '

max_length = int(input("Enter the maximum password length: "))

outfile = path.join(fpath, "tmp.txt")  # <- Korrekte Pfadverkettung

with open(outfile, "w", encoding="utf-8") as f:
    for length in range(1, max_length + 1):
        for combination in product(charset, repeat=length):
            password = ''.join(combination)
            f.write(password + '\n')

print(f"Passwords saved to: {outfile}")
