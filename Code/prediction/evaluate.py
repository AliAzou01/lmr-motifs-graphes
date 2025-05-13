from prediction.markov_from_patterns import *
from prediction.markov_from_sequences import *

def read_spmf_sequences(file_path):
    """Lit un fichier SPMF et retourne une liste de séquences (chaque séquence est une liste d'IDs en string)."""
    sequences = []
    with open(file_path, "r") as f:
        for line in f:
            tokens = line.strip().split()
            sequence = []
            for token in tokens:
                if token == "-1":
                    continue  # séparateur d'itemset, ignoré si pas utilisé
                elif token == "-2":
                    if sequence:
                        sequences.append(sequence)
                        sequence = []
                else:
                    sequence.append(token)
            if sequence:
                sequences.append(sequence)
    return sequences

def decode_sequences(encoded_sequences, id_to_port):
    """Convertit les IDs en noms de ports selon un mapping fourni."""
    decoded = []
    for seq in encoded_sequences:
        decoded_seq = [id_to_port.get(int(item), f"UNKNOWN({item})") for item in seq]
        decoded.append(decoded_seq)
    return decoded


def evaluate_prediction_on_test_sequence(test_sequence, transition_probabilities, x):
    score = 0
    total = 0
    for i in range(x, len(test_sequence)):
        context = tuple(test_sequence[i - x:i])
        actual_next = test_sequence[i]
        if context in transition_probabilities:
            predicted_port = max(transition_probabilities[context], key=lambda t: t[1])[0]
            # print("context: ", context, ", actual next: ", actual_next, ", predicted next: ", predicted_port)
            if predicted_port == actual_next:
                # print("score ++")
                score += 1
            total += 1
    return score, total

def evaluate_multiple_sequences(test_sequences, transition_probabilities, x):
    total_score = 0
    total_predictions = 0
    for seq in test_sequences:
        # print(seq)
        score, total = evaluate_prediction_on_test_sequence(seq, transition_probabilities, x)
        total_score += score
        total_predictions += total
    if total_predictions == 0:
        return 0, 0, 0.0
    average_precision = total_score / total_predictions
    return total_score, total_predictions, average_precision
