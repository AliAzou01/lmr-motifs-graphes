import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from prediction.markov_from_sequences import compute_transition_probabilities_from_sequences
from prediction.sequence_splitter import read_sequences, write_sequences, split_sequences
from prediction.evaluate import evaluate_multiple_sequences
from models.baseEntier import load_json
from prediction.markov_from_sequences import decode_sequences,read_spmf_sequences

"""
Description du script :
Ce script exécute une validation croisée sur un modèle de chaînes de Markov construit à partir des séquences de ports brutes,
sans extraction de motifs. Il divise les données, construit un modèle de transition d'ordre n, et évalue les prédictions
sur les séquences de test.

Les résultats sont agrégés sur K folds pour produire une évaluation moyenne.
"""

# === CONFIGURATION ===
INPUT_FILE = "text_files/spmf_input.txt"

while True:
    try:
        ORDER = int(input("Veuillez entrer l'ordre de la chaîne de Markov (un entier >= 1) : "))
        if ORDER >= 1:
            break
        else:
            print("L'ordre doit être un entier strictement supérieur ou égal à 1.")
    except ValueError:
        print("Entrée invalide. Veuillez entrer un entier valide.")

# === FICHIERS TEMPORAIRES ===
TRAIN_FILE = "text_files/temp_train.txt"
TEST_FILE = "text_files/temp_test.txt"

def run_cross_validation():
    """Effectue la validation croisée sur chaînes de Markov basées sur des séquences complètes (brutes)."""
    sequences = read_sequences(INPUT_FILE)
    scores = []

    K = int(1 / (1 - 0.8))  # Si 80% entraînement, alors K = 5

    for fold in range(K):
        print(f"\n[Fold {fold + 1}/{K}]")
        
        if fold == 0:
            train_sequences, test_sequences = split_sequences(sequences, train_ratio=0.8, test_window_index=fold, shuffle=True, seed=2)
        else:
            train_sequences, test_sequences = split_sequences(sequences, train_ratio=0.8, test_window_index=fold, shuffle=False)

        write_sequences(train_sequences, TRAIN_FILE)
        write_sequences(test_sequences, TEST_FILE)

        # Charger le mapping ID → nom de port
        port_to_id = load_json("../Data/port_mapping.json")
        id_to_port = {v: k for k, v in port_to_id.items()}

        # Lire et décoder les séquences
        train_encoded = read_spmf_sequences(TRAIN_FILE)
        train_sequences = decode_sequences(train_encoded, id_to_port)

        test_encoded = read_spmf_sequences(TEST_FILE)
        test_sequences = decode_sequences(test_encoded, id_to_port)

        # Modèle de Markov sur séquences brutes
        transition_probabilities = compute_transition_probabilities_from_sequences(train_sequences, order=ORDER)

        # Évaluation
        score, total, avg = evaluate_multiple_sequences(test_sequences, transition_probabilities, x=ORDER)
        avg_prec = score / total * 100

        print(f"\nScore total : {score}/{total} → Précision moyenne : {avg_prec:.2f}%")
        scores.append(avg_prec)
        print(f"[Score] Fold {fold+1}: {avg_prec:.4f}%")

    # Résumé final
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    print("\n[FINISHED CROSS-VALIDATION]")
    print(f"Moyenne : {mean_score:.4f}%")
    print(f"Écart type : {std_score:.4f}%")

if __name__ == "__main__":
    run_cross_validation()
