"""docs.python.org/3/refrences/datamodel.html#special-method-names
"""
class Vault:
    def __init__(self, galleons=0, sickless=0, knuts=0):
        self.galleons = galleons
        self.sickless = sickless
        self.knuts = knuts
    
    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickless} Sickless, {self.knuts} Knuts"
    
    def __add__(self, other):
        galleons = self.galleons + other.galleons
        sickless = self.sickless + other.sickless
        knuts = self.knuts + other.knuts
        return Vault(galleons, sickless, knuts)

potter = Vault(100, 50, 25)
print(potter)

weasley = Vault(25, 50, 100)
print(weasley)

total = potter + weasley
print(total)