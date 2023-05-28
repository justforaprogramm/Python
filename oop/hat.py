import random as rn
class Hat:
    
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
        
    @classmethod
    def sort(cls, name):
        print(name, "is in", rn.choice(cls.houses))
    
    

Hat.sort("Harry")