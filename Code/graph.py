import networkx as nx
import matplotlib.pyplot as plt
import sys
from matplotlib.patches import Patch

def parse_sequence(sequence_data):
    """
    Analyse les données de séquence pour extraire les arêtes 
    (connexions entre les ports).
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
    Crée un graphe orienté à partir des arêtes fournies et l'affiche 
    avec des couleurs spécifiques pour les nœuds.
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Identification du premier et du dernier nœud
    first_node = edges[0][0]
    last_node = edges[-1][1]

    # Couleurs des nœuds : vert pour le premier, rouge pour le dernier,
    # orange s'il s'agit du même nœud, et bleu pour les autres
    node_colors = []
    for node in G.nodes:
        if node == first_node and node == last_node:
            node_colors.append("orange")  # Nœud départ = arrivée
        elif node == first_node:
            node_colors.append("green")  # Nœud de départ
        elif node == last_node:
            node_colors.append("red")  # Nœud final
        else:
            node_colors.append("skyblue")  # Nœuds intermédiaires

    # Affichage des données pour le débogage
    print(f"Sequence {sequence_number} - Arêtes :", G.edges)

    # Dessiner le graphe avec les couleurs des nœuds
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)  # Utilisation d'un layout lisible
    nx.draw(
        G, pos, with_labels=True, node_color=node_colors, node_size=3000,
        font_size=10, font_weight="bold", arrowsize=20, edge_color="gray"
    )

    # Ajouter une légende pour expliquer les couleurs des nœuds
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

    # Ajouter un titre au graphe
    plt.title(f"Graphe pour la séquence {sequence_number}")
    plt.show()

def read_sequence_from_file(filename, sequence_number):
    """
    Lit les données de séquence depuis un fichier et retourne 
    la séquence correspondant au numéro donné.
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    
    sequence_data = None
    for line in lines:
        # Recherche de la séquence correspondant au numéro donné
        if line.startswith(f"Sequence {sequence_number}:"):
            sequence_data = line.strip().split(":", 1)[1].strip()
            break
    
    if not sequence_data:
        raise ValueError(f"Sequence {sequence_number} introuvable dans le fichier.")
    
    return sequence_data

if __name__ == "__main__":
    # Vérifie si un numéro de séquence est passé en argument
    if len(sys.argv) != 2:
        print("Erreur : Nombre d'arguments incorrect")
        print("Usage : python3 script.py <numéro_de_séquence>")
        sys.exit(1)

    # Lire le numéro de séquence depuis les arguments
    sequence_number = int(sys.argv[1])
    
    # Lire la séquence depuis le fichier
    filename = "text_files/sequences_from_to.txt"
    sequence_data = read_sequence_from_file(filename, sequence_number)
    
    # Analyser et créer le graphe pour la séquence donnée
    edges = parse_sequence(sequence_data)
    create_graph(edges, sequence_number)
