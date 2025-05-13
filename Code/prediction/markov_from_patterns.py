import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

""" 
Description du script :
Ce script calcule les probabilités de transition d'une chaîne de Markov à partir des motifs extraits 
par un algorithme tel que PrefixSpan. Il génère ensuite une matrice de transition, la visualise avec un 
diagramme de chaleur (heatmap) et l'enregistre dans un fichier PNG. Ce processus est utilisé pour modéliser 
les transitions entre différents états (séquences de ports).
"""

def plot_transition_matrix(transition_probabilities,file_name):
    """
    Trace la matrice de transition sous forme de heatmap et l'enregistre dans un fichier PNG.

    Args:
        transition_probabilities (dict): Dictionnaire des probabilités de transition (état précédent -> port de destination -> probabilité).
    """
    # Déterminer l'ordre de la chaîne à partir des longueurs des clés
    sample_key = next(iter(transition_probabilities))
    order = len(sample_key)

    # Extraire tous les ports uniques (sources et destinations)
    ports = sorted(set(p for key in transition_probabilities for p in key) |
                   set(p for values in transition_probabilities.values() for p, _ in values))

    # Créer des étiquettes lisibles pour les états (séquences de ports)
    state_keys = list(transition_probabilities.keys())
    state_labels = ['→'.join(map(str, state)) for state in state_keys]

    # Initialiser la matrice
    matrix = np.zeros((len(state_keys), len(ports)))

    # Indices des ports pour colonnes
    port_idx = {port: i for i, port in enumerate(ports)}

    # Remplir la matrice avec les probabilités
    for row_idx, key in enumerate(state_keys):
        for port, prob in transition_probabilities[key]:
            col_idx = port_idx[port]
            matrix[row_idx, col_idx] = prob

    # Tracer la matrice
    plt.figure(figsize=(12, len(state_keys) * 0.5 + 2))
    ax = sns.heatmap(matrix, annot=True, cmap="Blues",
                     xticklabels=ports,
                     yticklabels=state_labels,
                     cbar_kws={'label': 'Probabilité'})

    ax.set_xlabel("Port de destination")
    ax.set_ylabel(f"État précédent (ordre {order})")
    plt.title(f"Matrice de transition de la chaîne de Markov (ordre {order})")
    plt.tight_layout()
    plt.savefig(f"../Data/{file_name}.png")
    print(f"Matrice enregistrée dans '../Data/{file_name}.png'")


def compute_transition_probabilities(sequences, order=2):
    """
    Calcule les probabilités de transition pour une chaîne de Markov à partir des séquences de motifs.

    Args:
        sequences (list): Liste des séquences avec leurs supports.
        order (int): L'ordre de la chaîne de Markov.

    Returns:
        dict: Dictionnaire des probabilités de transition (état précédent -> port de destination -> probabilité).
    """
    if order < 1:
        raise ValueError("L'ordre de la chaîne de Markov doit être au moins 1.")

    transition_counts = defaultdict(lambda: defaultdict(int))

    # Calcul des transitions entre les états
    for item in sequences:
        sequence = item["sequence"]
        support = item["support"]

        if len(sequence) < order + 1:
            continue

        for i in range(len(sequence) - order):
            key = tuple(sequence[i:i + order])  # Séquence d'état précédent
            next_port = sequence[i + order]  # Port suivant
            transition_counts[key][next_port] += support

    # Calcul des probabilités de transition
    transition_probabilities = {}
    for key, next_ports in transition_counts.items():
        total = sum(next_ports.values())
        transition_probabilities[key] = [
            (port, count / total) for port, count in next_ports.items()
        ]

    return transition_probabilities

# === Bloc principal ===
if __name__ == "__main__":
    # Chargement des séquences
    try:
        with open("../Data/output_sequences.json", "r") as f:
            sequences = json.load(f)
    except FileNotFoundError:
        print("Le fichier 'output_sequences.json' est introuvable.")
        exit()

    # Demande à l'utilisateur de saisir l'ordre
    while True:
        try:
            order = int(input("Entrez l'ordre de la chaîne de Markov (≥ 1) : "))
            if order >= 1:
                break
            else:
                print("Veuillez entrer un entier supérieur ou égal à 1.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un entier.")

    # Calcul des probabilités de transition
    transition_probabilities = compute_transition_probabilities(sequences, order=order)

    #plot_transition_matrix(transition_probabilities,"matrice_transition_patern")

    # Affichage textuel des résultats
    for key, values in transition_probabilities.items():
        print(f"\nSi le navire était à {key}, il ira probablement vers :")
        for port, prob in values:
            print(f"  - {port} avec une probabilité de {prob:.2f}")
