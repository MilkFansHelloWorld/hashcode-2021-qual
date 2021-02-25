import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
import math
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
    # Note street frequency
    street_freqs = {}
    for p in ns.paths.values():
        for st_name in p.st_names:
            if st_name not in street_freqs:
                street_freqs[st_name] = 0
            street_freqs[st_name]+=1
    output = {}
    for E, incoming_streets in graph.adj_list_to_E.items():
        output[E] = {'E_i':len(incoming_streets), 'street': incoming_streets}
    res = []
    res.append(len(output))
    for E, o in output.items():
        # check which streets are the most frequently used
        #street_list = [(street.name, street_freqs.get(street.name, 0)) for (street, _) in o['street']]
        street_list = []
        for (street, _) in o['street']:
            if not (street.name not in street_freqs or street_freqs[street.name]==0):
                street_list.append((street.name, street_freqs[street.name]))
        if len(street_list) < 1:
            res[0]-=1
        else:
            res.append(E)
            res.append(len(street_list))
            street_list.sort(key=lambda el: el[1], reverse=True)
            # print(street_list)
            # max_freq = street_list[0][1]
            # min_freq = street_list[-1][1]
            #street_list_corrected = [(street_name, freq) for (index, (street_name, freq)) in enumerate(street_list)]
            # street_list_corrected = [(street_name, 1) for (index, (street_name, freq)) in enumerate(street_list)]
            street_list_corrected = []
            if len(street_list) > 1 and street_list[0][1] > 5*street_list[1][1]:
                street_list_corrected = [(street_name, freq) for (index, (street_name, freq)) in enumerate(street_list)]
            else:
                street_list_corrected = [(street_name, 4-int(index/3)) for (index, (street_name, freq)) in enumerate(street_list)]
            # street_list_corrected = [(street_name, max(1, int(lambda_val*math.exp(-lambda_val*index)))) for (index, (street_name, freq)) in enumerate(street_list)]
            for (street_name, corrected_freq) in street_list_corrected:
                res.append('{} {}'.format(street_name, max(corrected_freq, 1)))
    return '\n'.join(map(str, res))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print(out)

