from typing import List
import pandas as pd
import json


def stateToList(state: str) -> List[int]:
    a = state.split(" ")[:-1]
    a[0] = a[0][1:]
    a = [int(x) for x in a]
    return a

with open("./mincov_out_0_.json") as f:
    fileJSON = json.load(f)
    # states = [ '[ 0 1 0 ... ]', '[ 1 0 0 ...]', ... ]
    states =  [stateToList(x["state"]) for x in fileJSON["nodes"]]
    print(states)

