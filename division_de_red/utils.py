from typing import List
from itertools import compress, product



def set_to_string(items):
    string_set = '-'.join(list([str(num) for num in items]))
    return string_set

def list_to_string(lista: List[int]) -> str:
    return "[" + ", ".join([str(elem) for elem in lista]) + " ]"

def combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )