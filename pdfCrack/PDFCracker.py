from PyPDF2 import PdfReader
from itertools import product
import string
from os import path

# Pfad & Dateieingabe
fpath = path.dirname(path.abspath(__file__))
ifile = path.join(fpath, input("Enter the file name of the PDF to crack: "))

# Zeichensatz und maximale Passwortlänge
charset = string.digits + string.ascii_letters + string.punctuation + ' '
max_length = int(input("Enter maximum password length to try: "))

try:
    with open(ifile, 'rb') as file:
        reader = PdfReader(file)
        if not reader.is_encrypted:
            print("The PDF isn't encrypted.")
            exit()

        for length in range(1, max_length + 1):
            for count, combination in enumerate(product(charset, repeat=length), start=1):
                password = ''.join(combination)
                result = reader.decrypt(password)

                if result == 1:
                    print(f"Password found: '{password}' (Attempt {count})")
                    exit()
                if count % 10000 == 0:
                    print(f"Tried {count} passwords...")

        print("No valid password found.")

except FileNotFoundError:
    print(f"File {ifile} not found.")
    exit()
