import itertools as it
import networkx as nx
import numpy as np
import math

def check_same_direction(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    if (x1 > 0 and x2 > 0) or (x1 < 0 and x2 < 0):
        if (y1 > 0 and y2 > 0) or (y1 < 0 and y2 < 0):
            return True
    elif (y1 > 0 and y2 > 0) or (y1 < 0 and y2 < 0):
        if (x1 > 0 and x2 > 0) or (x1 < 0 and x2 < 0):
            return True
    return False


def angle_between_vectors(u, v):
    if u[0]*v[1] == u[1]*v[0]:
        return 0 if check_same_direction(u, v) else math.pi
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot_product / (norm_u * norm_v)
    theta = np.arccos(cos_theta)
    return theta

def compute_angle_wait(perm, pos, C):
    current_vec = (0,1)
    wait = 0
    for (u, v) in zip(perm[:-1], perm[1:]):
        next_vec = (pos[v][0] - pos[u][0], pos[v][1] - pos[u][1])
        angle = angle_between_vectors(current_vec, next_vec)
        wait += angle * C
        current_vec = next_vec
    return wait

def iter_path(G):
    start = list(G.nodes())[0]
    nodes = list(G.nodes())[1:]
    for p in it.permutations(nodes):
        yield [start] + list(p) + [start]

def tsp_brute_force(G, pos, C):
    min_dist = 10e30
    ret = None
    for p in iter_path(G):
        length = 0
        length += compute_angle_wait(p, pos, C)
        for (u, v) in zip(p[:-1], p[1:]):
            if (w := G.get_edge_data(u, v)) != None:
                length += w["weight"]
            else:
                length += 10e40
        if length < min_dist:
            ret = p
            min_dist = length
    return ret

def get_edge_from_perm(perm, edge_paths={}):
    l = []
    for edge in zip(perm[:-1], perm[1:]):
        if edge in edge_paths:
            l += get_edge_from_perm(edge_paths[edge])
        else:
            l += [edge]
    return l