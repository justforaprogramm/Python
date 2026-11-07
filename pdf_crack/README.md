# PDF cracker

## Overview

Scripts to encrypt a PDF (`PDFEncrypter.py`) and to brute-force the password of a PDF you own (`PDFCracker.py`). Only use it on your own files.

## Original notes

this is my personal PDF Cracker.
I had a file encrypted which i forgot the Password.

<br>
<b>THIS IS NOT FOR ILLIGAL USECASES!!!</b>
<br>

perl .\dir\john-1.9.0-jumbo-1-win64\run\pdf2john.pl C:\dir\tmp-Out.pdf > C:\dir\hash.txt
use vscode or notepad++ to change hashcode to utf-8 (without bom)

C:\dir\hashcat-6.2.6
hashcat -m 10500 -a 3 C:\dir\hash.txt ?a
