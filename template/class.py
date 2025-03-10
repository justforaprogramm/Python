from email.headerregistry import Address


class person():
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __str__(self):
        return f"{self.name} from {self.address}"
    
    @classmethod
    def get(cls):
        name = input("Name: ")
        address = input("address: ")
        return cls(name, address)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name
        
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if not address:
            raise ValueError("Missing address")
        self._address = address

def main() -> None:
    """call class
    """
    ps = person.get()
    print(ps)


if __name__ == "__main__":
    main()
