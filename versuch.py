#def main():
#    sec = int(input("Sekunden: "))
#    min = sec / 60
#    sec = sec % 60
#    print(f"minuten: {int(min)} \n secunden: {sec}")
#   
#if __name__ == "__main__":    
#    main()
from re import sub as resub

def check(text: str) -> bool:
        """Return True if *text* is a palindrome (ignores spaces, punctuation, case)."""
        cleaned = lambda text: resub(r"[^a-zA-Z0-9]", "", text).lower()
        test = cleaned(text)
        return test == test[::-1]
        
if __name__ == "__main__":    
    print(check("test tset"))
