import networkx as nx
import matplotlib.pyplot as plt
import math
from tsp import tsp_brute_force
from load import load

def get_edge_from_perm(perm):
    l = []
    for edge in zip(perm[:-1], perm[1:]):
        l += [edge]
    return l

def show_robot_path(coords, C=0):
    # Créer un graphe complet avec des poids égaux à la distance euclidienne entre les nœuds
    n = len(coords)
    G = nx.complete_graph(n)
    for (u, v, w) in G.edges(data=True):
        dist = math.sqrt((coords[u][0]-coords[v][0])**2 + (coords[u][1]-coords[v][1])**2)
        w['weight'] = dist

    min_perm = tsp_brute_force(G, coords, C)
    min_edges = get_edge_from_perm(min_perm)
    print(f"Best path : {min_perm}")

    H = nx.Graph()
    H.add_edges_from(min_edges)

    fig, ax = plt.subplots()
    pos = dict(zip(range(n), coords))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=0.5, edge_color='grey')
    nx.draw_networkx_edges(H, pos, width=2.0, edge_color='blue')
    plt.axis('off')
    plt.grid(True)
    plt.show()

# Créer une liste de coordonnées de nœuds
coords = [(0, 0), (1, 2), (3, 1), (2, 4), (4, 3), (2, 2), (3, 3)]
show_robot_path(load("data.txt")[1], 0)