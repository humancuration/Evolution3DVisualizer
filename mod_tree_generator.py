# mod_tree_generator.py

import networkx as nx
import numpy as np
from util_math import calculate_genetic_distance

def generate_tree(processed_data):
    """
    Generates an evolutionary tree structure with 3D positions.

    Parameters:
        processed_data (dict): Processed data containing species and distance matrix.

    Returns:
        networkx.Graph: Graph representing the evolutionary tree with 3D positions.
    """
    species = processed_data['species']
    distance_matrix = processed_data['distance_matrix']
    
    # Create a graph
    G = nx.Graph()
    
    # Add nodes
    for sp in species:
        G.add_node(sp)
    
    # Add edges with genetic distance as weight
    for sp1 in species:
        for sp2 in species:
            if sp1 != sp2:
                distance = distance_matrix[sp1][sp2]
                if distance >= 0:
                    G.add_edge(sp1, sp2, weight=distance)
    
    # Compute 3D positions using spring layout
    pos = nx.spring_layout(G, dim=3, weight='weight', seed=42)
    
    # Assign positions to nodes
    for node in G.nodes():
        G.nodes[node]['pos'] = pos[node]
    
    return G
