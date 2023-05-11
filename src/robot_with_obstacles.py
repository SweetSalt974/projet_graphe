import networkx as nx
import matplotlib.pyplot as plt
import math
from tsp import tsp_brute_force
from load import load
from obstacle import is_passing_through_any_obstacle

def show_board(coords, rectangles, C):
    # Créer un graphe complet avec des poids égaux à la distance euclidienne entre les nœuds
    n = len(coords)
    G = nx.complete_graph(n+len(rectangles) * 4)
    H = nx.Graph()
    rect_coords = []
    for i in range(len(rectangles)):
        H.add_nodes_from([i*4, i*4 + 1, i*4 + 2, i*4 + 3])
        H.add_edges_from([(i*4, i*4+1), (i*4, i*4+2), (i*4+1, i*4+3), (i*4+2, i*4+3)])
        rect_coords += [(rectangles[i][0][0], rectangles[i][0][1])]
        rect_coords += [(rectangles[i][1][0], rectangles[i][0][1])]
        rect_coords += [(rectangles[i][0][0], rectangles[i][1][1])]
        rect_coords += [(rectangles[i][1][0], rectangles[i][1][1])]

    coords_with_obstacle = coords + rect_coords
    edge_to_remove = []
    for (u, v, w) in G.edges(data=True):
        if is_passing_through_any_obstacle(coords_with_obstacle[u], coords_with_obstacle[v], rectangles) != None:
            edge_to_remove += [(u,v)]
            continue
        dist = math.sqrt((coords_with_obstacle[u][0]-coords_with_obstacle[v][0])**2 + (coords_with_obstacle[u][1]-coords_with_obstacle[v][1])**2)
        w['weight'] = dist
    G.remove_edges_from(edge_to_remove)
    

    fig, ax = plt.subplots()
    pos = dict(zip(range(n + len(rect_coords)), coords + rect_coords))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=0.5, edge_color='grey')

    #draw obstacle
    rect_pos = dict(zip(range(n), rect_coords))
    nx.draw_networkx_nodes(H, rect_pos, node_size=100, node_color='red')
    nx.draw_networkx_edges(H, rect_pos, width=1, edge_color="red")


    plt.axis('off')
    plt.grid(True)
    plt.show()

data = load("data2.txt")
print(data)
show_board(data[1], data[2], 0)