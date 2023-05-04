import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
import math

# Créer une liste de coordonnées de nœuds
coords = [(0, 0), (1, 2), (3, 1), (2, 4), (4, 3)]

# Créer un graphe complet avec des poids égaux à la distance euclidienne entre les nœuds
n = len(coords)
G = nx.complete_graph(n)
for (u, v, w) in G.edges(data=True):
    dist = math.sqrt((coords[u][0]-coords[v][0])**2 + (coords[u][1]-coords[v][1])**2)
    w['weight'] = dist

# Calculer toutes les permutations possibles des nœuds
perms = permutations(range(n))

# Trouver la permutation avec le coût minimum
min_cost = float('inf')
min_perm = None
for perm in perms:
    cost = sum(G[perm[i]][perm[(i+1)%n]]['weight'] for i in range(n))
    if cost < min_cost:
        min_cost = cost
        min_perm = perm

# Créer un sous-graphe avec la permutation trouvée
H = G.subgraph(min_perm)

# Dessiner le graphe et ajouter un quadrillage orthonormé
fig, ax = plt.subplots()
pos = dict(zip(range(n), coords))
nx.draw_networkx_nodes(G, pos, node_color='lightblue')
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_edges(H, pos, width=2.0, edge_color='black')
plt.axis('off')
plt.grid(True)
plt.show()
