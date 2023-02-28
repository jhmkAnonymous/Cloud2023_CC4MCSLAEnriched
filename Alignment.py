"""
    Checker 
"""
import pm4py
import json

### Get Discovered state-machine
SM_disc = json.load(open("SM_identified/SM_.json"))

### Get Defined state-machine
SM_Def = None

### Search Space construction
for elt in SM_disc:
    print(elt)


### Searching shortest path



