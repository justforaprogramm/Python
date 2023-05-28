"""docs.python.org/3/tutorial/classes.html
   raise
   now can make errorswith s.o.
   class int(x, base=10)
"""
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house
    
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
    def house(self):
        return self._house
    
    @house.setter
    def house(self, house):
        if house not in ["G", "H", "R", "S"]:
            raise ValueError("Invalid house")
        self._house = house

def main():
    student = Student.get()
    print(student)
    
if __name__ == "__main__":
    main()