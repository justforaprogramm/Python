import sys

def count_letter(word, letter):
    return word.count(letter)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Bitte geben Sie ein Wort und einen Buchstaben als Argumente ein.")
        sys.exit(1)
    
    word = sys.argv[1]
    letter = sys.argv[2]
    
    if len(letter) == 1:
        count = count_letter(word, letter)
        print(count)
    else:
        print("Bitte geben Sie nur einen Buchstaben ein.")
