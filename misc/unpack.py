#            default 0, kann verändert werden       
#                  v           v        v
def total(galleons=0, sickless=0, knuts=0):
    return (galleons * 17 + sickless) * 29 + knuts

#liste
coins = [100, 50, 25]
print(total(*coins), "Knuts")

#wörterbuch
coins = {"galleons": 100, "sickless": 50, "knuts": 25}

print(total(**coins), "knuts")