from PyPDF2 import PdfReader
from os import path

fpath = '\\'.join(path.abspath(__file__).split(path.sep)[:-1])
ifile = fpath + '\\' + input("Enter the file name of the PDF to crack: ")
passwordList = fpath + '\\tmp.txt'

try:
    with open(ifile, 'rb') as file:
        reader = PdfReader(file)
        if not reader.is_encrypted:
            print("The PDF isn't encrypted.")
            exit()

        with open(passwordList, 'r', encoding='utf-8') as f:
            for countlines, line in enumerate(f, start=1):
                password = line.strip()
                result = reader.decrypt(password)

                if result == 0:
                    ...
                else:
                    print(f"Password found: '{password}' (Line {countlines})")
                    exit()

        print("No valid password found.")

except FileNotFoundError:
    print(f"File {ifile} not found.")
    exit()