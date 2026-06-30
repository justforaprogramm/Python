import sys

def count_letter(word, letter):
    return word.count(letter)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Zählt die Anzahl der Vorkommen eines Buchstabens in einem Wort.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("wort", nargs='?', help="Das Wort, in dem gezählt werden soll")
    group.add_argument("-i", "--interactive", action="store_true", help="Interaktiver Modus")
    
    args = parser.parse_args()
    
    if args.interactive:
        word = input("Gebe ein Wort ein: ")
        letter = input("Gebe einen Buchstaben ein: ")
    elif args.wort is not None:
        word = args.wort
        letter = input("Gebe einen Buchstaben ein: ")
    else:
        print("Bitte geben Sie entweder ein Wort und einen Buchstaben oder verwenden Sie die Option -i für interaktiven Modus.")
        sys.exit(1)
    
    if len(letter) == 1:
        count = count_letter(word, letter)
        print(count)
    else:
        print("Bitte geben Sie nur einen Buchstaben ein.")
