import argparse
import json
from collections import *
from pathlib import Path

def ni(itr):
    return int(next(itr))

# parses the next string of itr as a list of integers
def nl(itr):
    return [int(v) for v in next(itr).split()]

class Street:
    def __init__(self, B, E, name, L):
        self.B = B
        self.E = E
        self.name = name
        self.L = L
        return

class Path_c:
    def __init__(self, P, street_name_ls):
        self.P = P
        self.st_names = street_name_ls
        return



def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()

    ns.D, ns.I, ns.S, ns.V, ns.F = nl(itr)
    streets = {}
    for _ in range(ns.S):
        temp = next(itr).split()
        B = int(temp[0])
        E = int(temp[1])
        name = temp[2]
        L = int(temp[3])
        streets[name] = Street(B, E, name, L)
    ns.streets = streets

    paths = {}
    for i in range(ns.V):
        temp = next(itr).split()
        P = int(temp[0])
        ls = temp[1:]
        paths[i] = Path_c(P, ls)
    ns.paths = paths

    return ns

class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)

def parse2json(inp):
    ns = parse(inp)
    return json.dumps(ns, cls=FlexibleEncoder)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    return parser.parse_args()

inp = '''6 4 5 2 1000
2 0 rue-de-londres 1
0 1 rue-d-amsterdam 1
3 1 rue-d-athenes 1
2 3 rue-de-rome 2
1 2 rue-de-moscou 3
4 rue-de-londres rue-d-amsterdam rue-de-moscou rue-de-rome
3 rue-d-athenes rue-de-moscou rue-de-londres'''

parse(inp)

