def count_letter(word, letter):
    return word.count(letter)

if __name__ == "__main__":
    word = input("Gebe ein Wort ein: ")
    letter = input("Gebe einen Buchstaben ein: ")
    
    if len(letter) == 1:
        count = count_letter(word, letter)
        print(f"Die Anzahl der Vorkommen von '{letter}' in '{word}' ist: {count}")
    else:
        print("Bitte gebe nur einen Buchstaben ein.")
