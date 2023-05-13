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
            length += G.get_edge_data(u, v)["weight"]
        if length < min_dist:
            ret = p
            min_dist = length
    return ret

def tsp_mst(G, C):
    MST = nx.minimum_spanning_tree(G)
    DFS_nodes = list(nx.dfs_postorder_nodes(MST))
    return tsp_2opt(DFS_nodes, G)

def tsp_2opt(solution, G):
    n = len(solution)
    amelioration = True
    while amelioration:
        meilleur_gain = 0
        amelioration = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                gain = G[solution[i-1]][solution[j]]["weight"] + G[solution[i]][solution[j+1]]["weight"] - G[solution[i-1]][solution[i]]["weight"] - G[solution[j]][solution[j+1]]["weight"]
                if gain < meilleur_gain:
                    # Inversion des sous-tournées entre i et j
                    solution[i:j+1] = reversed(solution[i:j+1])
                    meilleur_gain = gain
                    amelioration = True
    return solution

def get_edge_from_perm(perm, edge_paths={}):
    l = []
    for edge in zip(perm[:-1], perm[1:]):
        if edge in edge_paths:
            l += get_edge_from_perm(edge_paths[edge])
        else:
            l += [edge]
    return l

def get_perm_length(edges, pos, C):
    length = 0
    current_vec = (0,1)
    for (u, v) in edges:
        next_vec = (pos[v][0] - pos[u][0], pos[v][1] - pos[u][1])
        angle = angle_between_vectors(current_vec, next_vec)
        length += angle * C + math.sqrt((pos[u][0]-pos[v][0])**2 + (pos[u][1]-pos[v][1])**2)
        current_vec = next_vec
    return length
