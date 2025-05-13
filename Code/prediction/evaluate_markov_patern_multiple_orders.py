import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from prediction.markov_from_patterns import compute_transition_probabilities
from models.baseEntier import load_json
from prediction.evaluate import evaluate_multiple_sequences
from prediction.markov_from_sequences import read_spmf_sequences, decode_sequences
from prediction.markov_from_sequences import decode_sequences,read_spmf_sequences
from models.runPrefixSpan import run_prefixspan
from prediction.motif_to_json import parse_sequence_file

# === CONFIGURATION ===
ORDERS_TO_TEST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TRAIN_FILE = "text_files/sequence_train.txt"
TEST_FILE = "text_files/sequence_test.txt"
SPMF_OUTPUT = "text_files/spmf_output.txt"
SEQUENCES_JSON = "../Data/temp_parsed_output.json"

def run_evaluation_for_multiple_orders_motifs():
    # Charger le mapping port
    port_to_id = load_json("../Data/port_mapping.json")
    id_to_port = {v: k for k, v in port_to_id.items()}

    # Charger et décoder les séquences de test
    test_encoded = read_spmf_sequences(TEST_FILE)
    test_sequences = decode_sequences(test_encoded, id_to_port)

    print("\n=== ÉVALUATION À PARTIR DE MOTIFS POUR DIFFÉRENTS ORDRES ===")
    results = []

    # Générer les motifs à partir de l'entraînement
    print("[Étape 1] Extraction des motifs avec PrefixSpan...")
    run_prefixspan(id_to_port, spmf_input_file=TRAIN_FILE, spmf_output_file=SPMF_OUTPUT)

    print("[Étape 2] Parsing du fichier motifs en JSON...")
    parse_sequence_file("text_files/sequences.txt", SEQUENCES_JSON)

    try:
        with open(SEQUENCES_JSON, "r") as f:
            motifs = json.load(f)
    except FileNotFoundError:
        print("Le fichier JSON des motifs est introuvable.")
        return

    for order in ORDERS_TO_TEST:
        print(f"\n[Ordre {order}]")
        transition_probabilities = compute_transition_probabilities(motifs, order=order)
        score, total, avg = evaluate_multiple_sequences(test_sequences, transition_probabilities, x=order)
        # Vérifier la division par zéro
        if total > 0:
            precision = score / total * 100
        else:
            precision = 0.0  # Si aucun total, la précision est 0
        results.append((order, precision))
        print(f"Score : {score}/{total} → Précision : {precision:.2f}%")

    print("\n--- Résumé ---")
    for order, prec in results:
        print(f"Ordre {order} : {prec:.2f}%")

if __name__ == "__main__":
    run_evaluation_for_multiple_orders_motifs()
