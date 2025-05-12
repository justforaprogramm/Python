from PyPDF2 import PdfWriter, PdfReader
from os import path
fpath:str = '\\'.join(path.abspath(__file__).split(path.sep)[:-1])

ifile:str = fpath + '\\tmp.pdf'
ofile:str = ''
password:str = ''
writer = PdfWriter()

try: 
    with open(ifile, 'rb') as file:
        reader = PdfReader(file)
        if reader.is_encrypted:
            print("The PDF is already encrypted.")
            exit()

        password:str = input("Enter password for new PDF: ")
        ofile:str = ifile.split('.')[0] + '-Out.pdf'

        writer.clone_document_from_reader(reader)
    writer.encrypt(password)
        
    with open(ofile, 'wb') as file:
        writer.write(file)

except FileNotFoundError:
    print(f"File {ifile} not found.")
    exit()