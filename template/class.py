class person():
    def __init__(self, name, adress):
        self.name = name
        self.adress = adress
    
    def __str__(self):
        return f"{self.name} from {self.house}"
    
    @classmethod
    def get(cls):
        name = input("Name: ")
        house = input("House: ")
        return cls(name, house)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name
        
    @property
    def adress(self):
        return self._adress
    
    @adress.setter
    def house(self, house):
        self._adress = adress

def main() -> None:
    """call class
    """
    ps = person.get()
    print(ps)


if __name__ == "__main__":
    main()