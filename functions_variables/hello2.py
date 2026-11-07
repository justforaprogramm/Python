def main():
    hello()
    name = input("What's your name? ").strip().capitalize()
    hello(name)
    
    
def hello(to = "world"):
    print("hello, ", to, "!",sep="")
    
main()