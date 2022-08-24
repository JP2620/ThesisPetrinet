from typing import List
import pandas as pd
import json


# como verga pasamos de esas cadenas a un array pepegaHmm
# parseemos esta poronga auna lista y a mimir
def stateToList(state: str) -> List[int]:
    a = state.split(" ")[:-1]
    a[0] = a[0][1:]
    a = [int(x) for x in a]
    return a

# ahora qué? mimir?
with open("./mincov_out_0_.json") as f:
    fileJSON = json.load(f)
    # states = [ '[ 0 1 0 ... ]', '[ 1 0 0 ...]', ... ]
    states =  [x["state"] for x in fileJSON["nodes"]]
    print(stateToList(states[0]))

