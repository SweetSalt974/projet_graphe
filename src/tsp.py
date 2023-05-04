import itertools as it
import networkx as nx

def iter_path(G):
    start = list(G.nodes())[0]
    nodes = list(G.nodes())[1:]
    for p in it.permutations(nodes):
        yield [start] + list(p) + [start]

def tsp_brute_force(G):
    min_dist = 10e30
    ret = None
    for p in iter_path(G):
        length = 0
        for (u, v) in zip(p[:-1], p[1:]):
            length += G.get_edge_data(u, v)["weight"]
        if length < min_dist:
            ret = p
            min_dist = length
    return ret