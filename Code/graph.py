import networkx as nx
import matplotlib.pyplot as plt
import sys
from matplotlib.patches import Patch

def parse_sequence(sequence_data):
    """
    Parse the sequence data to extract edges (connections between ports).
    """
    edges = []
    for itemset in sequence_data.split(" -> "):
        from_node = None
        to_node = None
        for part in itemset.strip("<>{}").split():
            if "from:" in part:
                from_node = part.split(":")[1]
            if "to:" in part:
                to_node = part.split(":")[1]
        if from_node and to_node:
            edges.append((from_node, to_node))
    return edges

def create_graph(edges, sequence_number):
    """
    Create a directed graph from the edges and display it with custom node colors.
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Identifying the first and last nodes
    first_node = edges[0][0]
    last_node = edges[-1][1]

    # Node colors: green for the first node, red for the last node, orange if they are the same, and blue for others
    node_colors = []
    for node in G.nodes:
        if node == first_node and node == last_node:
            node_colors.append("orange")  # Same node for start and end
        elif node == first_node:
            node_colors.append("green")  # Start node
        elif node == last_node:
            node_colors.append("red")  # End node
        else:
            node_colors.append("skyblue")  # Intermediate nodes

    # Affichage des données pour débogage
    print(f"Sequence {sequence_number} - Arêtes :", G.edges)

    # Dessiner le graphe avec les couleurs des nœuds
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)  # Utiliser un layout plus lisible
    nx.draw(
        G, pos, with_labels=True, node_color=node_colors, node_size=3000,
        font_size=10, font_weight="bold", arrowsize=20, edge_color="gray"
    )

    # Ajouter une légende
    legend_elements = [
        Patch(facecolor="green", edgecolor="black", label="Nœud de départ"),
        Patch(facecolor="red", edgecolor="black", label="Nœud final"),
        Patch(facecolor="orange", edgecolor="black", label="Nœud départ = arrivée"),
        Patch(facecolor="skyblue", edgecolor="black", label="Nœud intermédiaire"),
    ]
    plt.legend(
        handles=legend_elements, loc="best", fontsize=12, title="Légende",
        title_fontsize=14, frameon=True
    )

    plt.title(f"Graphe pour la séquence {sequence_number}")
    plt.show()

def read_sequence_from_file(filename, sequence_number):
    """
    Read the sequence data from the file and return the specific sequence based on sequence_number.
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    
    sequence_data = None
    for line in lines:
        # Looking for the correct sequence number
        if line.startswith(f"Sequence {sequence_number}:"):
            sequence_data = line.strip().split(":", 1)[1].strip()
            break
    
    if not sequence_data:
        raise ValueError(f"Sequence {sequence_number} not found in the file.")
    
    return sequence_data

if __name__ == "__main__":
    # Vérifier si un numéro de séquence est passé en argument
    if len(sys.argv) != 2:
        print("Error: False number of args")
        print("Usage: python3 script.py <sequence_number>")
        sys.exit(1)

    # Lire le numéro de séquence passé en argument
    sequence_number = int(sys.argv[1])
    
    # Lire la séquence depuis le fichier
    filename = "sequences_output.txt"
    sequence_data = read_sequence_from_file(filename, sequence_number)
    
    # Parser et créer le graphe pour la séquence donnée
    edges = parse_sequence(sequence_data)
    create_graph(edges, sequence_number)
