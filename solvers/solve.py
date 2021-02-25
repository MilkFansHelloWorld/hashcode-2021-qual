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
        self.adj_list = {}
        for street in edges:
            if street.B not in self.adj_list:
                self.adj_list[street.B] = []
            self.adj_list[street.B].append((street, Queue()))
        self.vertices = self.adj_list.keys()
        self.edges = edges

def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    ns = parse(inp)

    return '0'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))

