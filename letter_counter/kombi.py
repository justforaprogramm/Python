def count_letter(word, letter):
    return word.count(letter)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Zählt die Anzahl der Vorkommen eines Buchstabens in einer Liste von Wörtern.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("woerter", nargs='*', help="Eine Liste von Wörtern, in denen gezählt werden soll")
    group.add_argument("-i", "--interactive", action="store_true", help="Interaktiver Modus")
    
    args = parser.parse_args()
    
    if args.woerter:
        woerter = args.woerter
    elif args.interactive:
        word = input("Gebe eine Liste von Wörtern ein, getrennt durch Leerzeichen: ")
        woerter = word.split()
    else:
        print("Bitte geben Sie entweder eine Liste von Wörtern oder verwenden Sie die Option -i für interaktiven Modus.")
        sys.exit(1)
    
    letter = input("Gebe einen Buchstaben ein: ")
    
    if len(letter) == 1:
        for wort in woerter:
            count = count_letter(wort, letter)
            print(f"In '{wort}' kommt der Buchstabe '{letter}' {count} mal vor.")
    else:
        print("Bitte geben Sie nur einen Buchstaben ein.")
