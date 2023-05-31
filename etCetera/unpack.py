def total(galleons, sickless, knuts):
    return (galleons * 17 + sickless) * 29 + knuts

coins = [100, 50, 25]
print(total(*coins), "Knuts")