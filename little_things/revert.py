def main(sequence) -> str:
    return '\x20'.join(reversed([i for i in sequence.split('\x20') if i]))

if '__main__' == __name__:
    sequence:str = input('enter a sentence: ')
    print(main(sequence))