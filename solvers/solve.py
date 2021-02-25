import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content
from queue import Queue

# inp is an input file as a single string
# return your output as a string

class Graph:
    def __init__(self, edges):
        self.adj_list_from_B = {}
        self.adj_list_to_E = {}
        for street_name, street in edges.items():
            if street.B not in self.adj_list_from_B:
                self.adj_list_from_B[street.B] = []
            street_queue_couple = (street, Queue())
            self.adj_list_from_B[street.B].append(street_queue_couple)
            if street.E not in self.adj_list_to_E:
                self.adj_list_to_E[street.E] = []
            self.adj_list_to_E[street.E].append(street_queue_couple)
        self.vertices = self.adj_list_from_B.keys()
        self.edges = edges

def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    ns = parse(inp)
    graph = Graph(ns.streets)
    output = {}
    for E, incoming_streets in graph.adj_list_to_E.items():
        output[E] = {'E_i':len(incoming_streets), 'street': incoming_streets}
    res = []
    res.append(len(output))
    for E, o in output.items():
        res.append(E)
        res.append(o['E_i'])
        for (street, q) in o['street']:
            res.append('{} {}'.format(street.name, 1))
    return '\n'.join(map(str, res))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print(out)

