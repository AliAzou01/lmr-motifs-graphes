import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import defaultdict
from models.baseEntier import load_json
from prediction.markov_from_patterns import plot_transition_matrix
"""
Description du script :
Ce script lit un fichier SPMF contenant des séquences de ports codées par des identifiants numériques,
les décode en noms de ports en utilisant un fichier de mapping, puis calcule les probabilités de transition 
d'une chaîne de Markov d'ordre n sur ces séquences. Le script permet de modéliser les transitions possibles 
entre les ports selon un ordre spécifié par l'utilisateur.
"""

def read_spmf_sequences(file_path):
    """Lit un fichier SPMF (séparateurs -1 et -2) et retourne une liste de séquences (de strings)."""
    sequences = []
    with open(file_path, 'r') as file:
        current_seq = []
        for token in file.read().split():
            if token == "-1":
                continue
            elif token == "-2":
                if current_seq:
                    sequences.append(current_seq)
                    current_seq = []
            else:
                current_seq.append(token)
        if current_seq:
            sequences.append(current_seq)
    return sequences

def decode_sequences(sequences, id_to_port):
    """Remplace les IDs par les noms des ports en utilisant le mapping."""
    decoded = []
    for seq in sequences:
        decoded_seq = [id_to_port.get(int(port_id), f"UNKNOWN({port_id})") for port_id in seq]
        decoded.append(decoded_seq)
    return decoded

def compute_transition_probabilities_from_sequences(sequences, order=2):
    """Calcule les probabilités de transition d'ordre n sur un ensemble de séquences."""
    transition_counts = defaultdict(lambda: defaultdict(int))

    for sequence in sequences:
        if len(sequence) <= order:
            continue
        for i in range(len(sequence) - order):
            key = tuple(sequence[i:i + order])
            next_port = sequence[i + order]
            transition_counts[key][next_port] += 1

    transition_probabilities = {}
    for key, next_ports in transition_counts.items():
        total = sum(next_ports.values())
        transition_probabilities[key] = [
            (port, count / total) for port, count in next_ports.items()
        ]
    
    return transition_probabilities

if __name__ == "__main__":
    try:
        order = int(input("Entrez l'ordre de la chaîne de Markov (>=1) : "))
        if order < 1:
            raise ValueError
    except ValueError:
        print("Entrée invalide. L'ordre doit être un entier >= 1.")
        exit(1)

    # Charger le mapping ID -> nom de port
    port_to_id = load_json("../Data/port_mapping.json")
    id_to_port = {v: k for k, v in port_to_id.items()}

    # Lire les séquences depuis le fichier SPMF
    spmf_sequences = read_spmf_sequences("text_files/sequence_train.txt")

    # Décoder les séquences en noms de ports
    decoded_sequences = decode_sequences(spmf_sequences, id_to_port)

    # Calculer les probabilités de transition d'ordre choisi
    transition_probabilities = compute_transition_probabilities_from_sequences(decoded_sequences, order=order)

    #plot_transition_matrix(transition_probabilities,"matrice_transition_sequence")

    # Affichage des transitions
    for key, next_ports in transition_probabilities.items():
        contexte = " → ".join(key)
        print(f"Si le navire était à {contexte}, il ira probablement vers :")
        for port, prob in next_ports:
            print(f"  - {port} avec une probabilité de {prob:.2f}")
        print()
