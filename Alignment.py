"""
    Checker 
"""
import pm4py
import json
import networkx as nx

### Get Discovered state-machine
SM_disc = json.load(open("SM_discovered/SM_.json"))

### Get Defined state-machine
SM_Def = None

### Search Space construction
SS = nx.DiGraph()
for elt in SM_disc:
    print(elt)


### Searching shortest path



