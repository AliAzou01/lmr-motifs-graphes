import json
import re

""" 
Description du script :
Ce script permet de parser un fichier contenant des séquences avec des motifs spécifiques et des supports associés,
puis de convertir ces séquences en un format JSON structuré. 
Le script ignore les lignes sans motifs et extrait les informations pertinentes via des expressions régulières.
"""

def parse_sequence_file(input_file_path, output_json_path):
    """
    Parse un fichier de séquences et enregistre les motifs et supports associés dans un fichier JSON.

    Args:
        input_file_path (str): Le chemin du fichier source contenant les séquences.
        output_json_path (str): Le chemin du fichier JSON de sortie.
    """
    sequences = []

    with open(input_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if "#SUP:" not in line:
                continue  # Ignorer les lignes sans motif

            # Extraire la séquence et le support avec une regex robuste
            match = re.match(r'^((?:\{[A-Z0-9]+\}(?: -> )?)*) #SUP: (\d+)', line)
            if match:
                raw_sequence, support = match.groups()
                items = re.findall(r'\{(.*?)\}', raw_sequence)
                sequences.append({
                    "sequence": items,
                    "support": int(support)
                })

    # Écriture dans un fichier JSON
    with open(output_json_path, 'w', encoding='utf-8') as out_file:
        json.dump(sequences, out_file, indent=2)

    print(f"{len(sequences)} motifs valides enregistrés dans '{output_json_path}'.")

# Exemple d’utilisation :
if __name__ == "__main__":
    input_path = "text_files/sequences.txt"
    output_path = "../Data/output_sequences.json"
    parse_sequence_file(input_path, output_path)
