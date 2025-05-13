import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prediction.markov_from_sequences import compute_transition_probabilities_from_sequences
from models.baseEntier import load_json
from prediction.evaluate import evaluate_multiple_sequences
from prediction.markov_from_sequences import read_spmf_sequences, decode_sequences

# === CONFIGURATION ===
ORDERS_TO_TEST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TRAIN_FILE = "text_files/sequence_train.txt"
TEST_FILE = "text_files/sequence_test.txt"

def run_evaluation_for_multiple_orders():
    # Charger le mapping ID -> nom port
    port_to_id = load_json("../Data/port_mapping.json")
    id_to_port = {v: k for k, v in port_to_id.items()}

    # Charger et décoder les séquences
    train_encoded = read_spmf_sequences(TRAIN_FILE)
    test_encoded = read_spmf_sequences(TEST_FILE)
    train_sequences = decode_sequences(train_encoded, id_to_port)
    test_sequences = decode_sequences(test_encoded, id_to_port)

    print("\n=== ÉVALUATION POUR DIFFÉRENTS ORDRES ===")
    results = []

    for order in ORDERS_TO_TEST:
        print(f"\n[Ordre {order}]")
        transition_probabilities = compute_transition_probabilities_from_sequences(train_sequences, order=order)
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
    run_evaluation_for_multiple_orders()
