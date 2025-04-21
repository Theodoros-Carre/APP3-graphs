import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def read_csv_graph(filename, directed=True):
    edges = []
    nodes = set()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or row[0].lower() == 'id1':
                continue  # skip empty rows and headers
            try:
                u, v = int(row[0]), int(row[1]) 
                edges.append((u, v))
                nodes.update([u, v])
                if not directed:
                    edges.append((v, u))
            except ValueError:
                print(f"Skipping invalid row: {row}")
    return list(nodes), edges

def create_adjacency_matrix(nodes, edges):
    size = max(nodes) + 1
    matrix = np.zeros((size, size), dtype=int)
    for u, v in edges:
        matrix[u][v] = 1
    return matrix

def save_matrix_to_file(matrix, filename):
    np.savetxt(filename, matrix, fmt='%d')

def find_leaders(matrix, directed=True, top_n=2):
    """Identify the most influential nodes (leaders) in the network.
        Directed Graphs: Counts how many nodes point to each node (column sums).
        Undirected Graphs: Counts connections per node (row sums, same as column sums)."""
    if directed:
        incoming = np.sum(matrix, axis=0)
    else:
        incoming = np.sum(matrix, axis=1)
    leaders = np.argsort(-incoming)[:top_n]
    return leaders.tolist(), incoming

def find_followers(matrix, node, directed=True):
    """Find all followers of a specific node.
        Directed: Checks the node's column for 1s (who follows it).
        Undirected: Checks the node's row ( same as neighbors)"""
    if directed:
        return list(np.where(matrix[:, node] == 1)[0])
    else:
        return list(np.where(matrix[node, :] == 1)[0])

def find_best_followers(matrix, top_n=2):
    """Identify nodes with the most outgoing connections.
        Counts how many nodes each node points to row sums"""
    outgoing = np.sum(matrix, axis=1)
    best_followers = np.argsort(-outgoing)[:top_n]
    return best_followers.tolist(), outgoing

def bfs_shortest_path(matrix, start, goal):
    """Find shortest path between nodes using BFS"""
    if start == goal:
        return [start]
    
    visited = set()
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node not in visited:
            neighbors = np.where(matrix[node] == 1)[0]
            
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                
                if neighbor == goal:
                    return new_path
                
                queue.append(new_path)
            
            visited.add(node)
    
    return None 


# Modify draw_graph to handle None paths
def draw_graph(nodes, edges, leaders, path=None):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, k=0.5, iterations=100)
    color_map = ['red' if node in leaders else 'skyblue' for node in G.nodes()]
    node_size = [800 if node in leaders else 300 for node in G.nodes()]

    plt.figure(figsize=(15, 10))
    nx.draw(G, pos, node_color=color_map, with_labels=True, 
           node_size=node_size, arrowsize=10, font_size=8)
    
    # Only draw path if one exists
    if path and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                              edge_color='green', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path,
                             node_color='green', node_size=500)

    plt.title("Social Network Graph", fontsize=14)
    plt.axis('off')
    plt.show()

#Choose
filename = 'club.txt'         
directed = False                  # True = direct graph , False = undirected graph
top_n_leaders = 3                # Number of leaders to find
top_n_followers = 5              # Number of best followers to find

#Run code
nodes, edges = read_csv_graph(filename, directed=directed)
matrix = create_adjacency_matrix(nodes, edges)
save_matrix_to_file(matrix, 'adjacency_matrix.txt')

leaders, _ = find_leaders(matrix, directed=directed, top_n=top_n_leaders)
for i, leader in enumerate(leaders):
    followers = [int(f) for f in find_followers(matrix, leader, directed=directed)]
    print(f"Leader {i+1} (node {leader}) followers:", followers)

best_followers, _ = find_best_followers(matrix, top_n=top_n_followers)
print("Best followers:", [int(bf) for bf in best_followers])


if len(leaders) >= 2:
    path = bfs_shortest_path(matrix, leaders[0], leaders[1])
    if path:
        print("Shortest path between leaders:", [int(p) for p in path])
    else:
        print(f"No path exists between leader {leaders[0]} and {leaders[1]}")
else:
    print("Not enough leaders to find a path")


draw_graph(nodes, edges, leaders)