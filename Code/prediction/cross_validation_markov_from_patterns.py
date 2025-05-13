import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import numpy as np
from prediction.markov_from_patterns import compute_transition_probabilities
from prediction.sequence_splitter import read_sequences, write_sequences, split_sequences
from prediction.motif_to_json import parse_sequence_file
from prediction.evaluate import evaluate_multiple_sequences
from models.runPrefixSpan import run_prefixspan
from models.baseEntier import load_json
from prediction.markov_from_sequences import decode_sequences,read_spmf_sequences

"""
Description du script :
Ce script effectue une validation croisée sur un modèle de chaînes de Markov construit à partir de motifs fréquents extraits 
par l'algorithme PrefixSpan. Pour chaque fold, il divise les séquences, extrait les motifs, construit une matrice de transition 
et évalue la performance du modèle sur les séquences de test.

Ce processus est répété K fois (cross-validation), et les scores moyens et écart-type sont affichés à la fin.
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
OUTPUT_SPMF = "text_files/spmf_output.txt"
OUTPUT_FILE = "text_files/outputfiltre.txt"
PARSED_JSON = "../Data/temp_parsed_output.json"

def run_cross_validation():
    """Effectue une validation croisée sur les chaînes de Markov générées à partir de motifs fréquents."""
    sequences = read_sequences(INPUT_FILE)
    scores = []

    K = int(1 / (1 - 0.8))  # K = 5 si test = 20%
    
    for fold in range(K):
        print(f"\n[Fold {fold + 1}/{K}]")
        
        if fold == 0:
            train_sequences, test_sequences = split_sequences(sequences, train_ratio=0.8, test_window_index=fold, shuffle=True, seed=2)
        else:
            train_sequences, test_sequences = split_sequences(sequences, train_ratio=0.8, test_window_index=fold, shuffle=False)
        
        write_sequences(train_sequences, TRAIN_FILE)
        write_sequences(test_sequences, TEST_FILE)

        port_to_id = load_json("../Data/port_mapping.json")
        port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

        test_encoded = read_spmf_sequences(TEST_FILE)
        test_sequences = decode_sequences(test_encoded, port_id_to_name)

        # Étape 1 : Extraction de motifs avec PrefixSpan
        _, _ = run_prefixspan(port_id_to_name, spmf_input_file=TRAIN_FILE, spmf_output_file=OUTPUT_SPMF)

        # Étape 2 : Parsing des motifs extraits
        parse_sequence_file("text_files/sequences.txt", PARSED_JSON)

        # Étape 3 : Construction de la matrice de transition
        try:
            with open(PARSED_JSON, "r") as f:
                sequences1 = json.load(f)
        except FileNotFoundError:
            print("Le fichier 'output_sequences.json' est introuvable.")
            exit()

        transition_probabilities = compute_transition_probabilities(sequences1, order=ORDER)

        # Étape 4 : Évaluation du modèle sur les séquences de test
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
