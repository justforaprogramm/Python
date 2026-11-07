"""generators
"""
def main():
    n = int(input("What's n? "))
    for s in sheep(n):
        print(s)

def sheep(n):
    for i in range(n):
        yield "🐏" * i #return but one value at a time
        
if __name__ =="__main__":
    main()