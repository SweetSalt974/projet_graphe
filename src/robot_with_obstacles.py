import networkx as nx
import matplotlib.pyplot as plt
import math
from tsp import *
from load import load
from obstacle import *

def show_robot_path(start, coords, rectangles, C=0):
    # Le graphe G contient les sommet des dechet et des rectangle, H juste les rectangles (pour le dessin)
    coords = [start] + coords
    n = len(coords)
    G = nx.complete_graph(n+len(rectangles) * 4)
    H = nx.Graph()
    rect_coords = []

    #Création du graphe contenant les obstacles
    for i in range(len(rectangles)):
        H.add_nodes_from([i*4, i*4 + 1, i*4 + 2, i*4 + 3])
        H.add_edges_from([(i*4, i*4+1), (i*4, i*4+2), (i*4+1, i*4+3), (i*4+2, i*4+3)])
        rect_coords += [(rectangles[i][0][0], rectangles[i][0][1])]
        rect_coords += [(rectangles[i][1][0], rectangles[i][0][1])]
        rect_coords += [(rectangles[i][0][0], rectangles[i][1][1])]
        rect_coords += [(rectangles[i][1][0], rectangles[i][1][1])]

    #Ajout des poids : Si on obstacle est sur l'arrete on l'ajoute à la liste des poids à A* et on met son poids à l'infini
    coords_with_obstacle = coords + rect_coords
    edge_to_compute = []
    for (u, v, w) in G.edges(data=True):
        if is_passing_through_any_obstacle(coords_with_obstacle[u], coords_with_obstacle[v], rectangles) != None:
            edge_to_compute += [(u,v)]
            w['weight'] = math.inf
        else:
            dist = math.sqrt((coords_with_obstacle[u][0]-coords_with_obstacle[v][0])**2 + (coords_with_obstacle[u][1]-coords_with_obstacle[v][1])**2)
            w['weight'] = dist

    edge_paths = {}

    #On calcul la distance des arrete qui sont coupé par un obstacle et on stocke le chemin emprunté pour chaque arrete
    for u, v in edge_to_compute:
        res = astar(u, v, coords_with_obstacle, G)
        # print(f"To go from {u} to {v}  path is {res[1]} and dist if {res[0]}")
        edge_paths[(u, v)] = res[1]
        G[u][v]['weight'] = res[0]
        edge_paths[(v, u)] = res[1][::-1]
        G[v][u]['weight'] = res[0]

    #On enlève les sommets des rectangles pour calculer la solution du TSP (comme on ne doit pas passer par eux)
    for node in list(G.nodes())[len(coords):]:
        G.remove_node(node)

    #Calcul de la solution (avec la 2_opt)
    opti_perm = tsp_mst(G, C)

    #Création du graphe solution (pour le dessin)
    L = nx.Graph()
    L.add_edges_from(get_edge_from_perm(opti_perm, edge_paths))

    #Dessin obstacle
    fig, ax = plt.subplots()
    rect_pos = dict(zip(range(n), rect_coords))
    nx.draw_networkx_nodes(H, rect_pos, node_size=10, node_color='red')
    nx.draw_networkx_edges(H, rect_pos, width=1, edge_color="red")

    #Dessin sommet dechets
    pos = dict(zip(range(n + len(rect_coords)), coords + rect_coords))
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color='lightblue')

    #Dessin Solution
    nx.draw_networkx_edges(L, pos, width=2.0, edge_color='blue')

    plt.axis('off')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    coords = [(0, 0), (1, 2), (3, 1), (2, 4), (3, 3), (4, 2), (1, 3)]
    rect = [[(2,1),(3,2)]]
    data = load("data2.txt")
    show_robot_path(data[0], data[1], data[2])