"""
experiment.py

Ce script exécute des expériences de minage de motifs séquentiels à partir de données de voyages maritimes.
Il utilise l’algorithme PrefixSpan via la librairie SPMF, applique un filtrage sur les motifs extraits, 
et calcule des métriques de performance et de complexité pour différentes valeurs de support minimum.

Sorties :
- Fichier contenant les motifs filtrés et traduits en noms de ports
- Fichier avec des statistiques (nombre de motifs, temps, taille moyenne, écart type)

Dépendances :
- SPMF (via run_spmf)
- NumPy
- Modules internes : baseEntier, decode_patterns, filter_motifs
"""

import os
import time
from datetime import datetime
import numpy as np

from Code.processing.decode_patterns import replace_ids_with_port_names
from Code.processing.filter_motifs import process_results
from models.baseEntier import load_json, transform_to_integer_database, write_spmf_file
from runAlgoSPMF import run_spmf


def calculate_metrics(patterns):
    """
    Calcule la taille moyenne et l’écart type des motifs.
    
    Args:
        patterns (List[str]): Liste des motifs sous forme de chaînes.
    
    Returns:
        tuple: (moyenne, écart type)
    """
    lengths = [len(pattern.split(" -1")) - 1 for pattern in patterns]
    mean_length = np.mean(lengths)
    std_dev = np.std(lengths)
    return mean_length, std_dev


if __name__ == "__main__":
    # === Préparation des données ===
    data = load_json("../Data/merged_voyages.json")
    port_to_id = load_json("../Data/port_mapping.json")
    db = transform_to_integer_database(data, port_to_id)
    write_spmf_file(db, "text_files/spmf_input_file.txt")

    spmf_input_file = "text_files/spmf_input_file.txt"
    port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

    # === Paramètres d'expérience ===
    min_supports = np.round(np.arange(0.02, 0.21, 0.01), 2)
    today_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs("experiment_results", exist_ok=True)

    metrics_file = f"./experiment_results/{today_datetime}_metrics.txt"
    patterns_file = f"./experiment_results/{today_datetime}_patterns.txt"

    # === Boucle principale des expériences ===
    with open(metrics_file, 'w') as metrics_f, open(patterns_file, 'w') as patterns_f:
        for min_support in min_supports:
            min_support_percentage = min_support * 100

            spmf_output_file = "text_files/output.txt"
            output_file_filtre = "text_files/outputfiltre.txt"

            # Lancer PrefixSpan
            start_time = time.time()
            run_spmf("PrefixSpan", spmf_input_file, spmf_output_file, f"{min_support_percentage}%")
            end_time = time.time()
            prefixspan_time_ms = (end_time - start_time) * 1000

            # Filtrage des motifs
            process_results(spmf_output_file, output_file_filtre)

            with open(output_file_filtre, 'r') as f:
                patterns = f.readlines()

            updated_patterns = replace_ids_with_port_names(patterns, port_id_to_name)

            # Calcul des métriques
            num_patterns = len(patterns)
            mean_length, std_dev = calculate_metrics(patterns)

            # Sauvegarde des métriques
            metrics_f.write(f"Support minimum: {min_support}\n")
            metrics_f.write(f"Temps pris (ms): {prefixspan_time_ms:.2f}\n")
            metrics_f.write(f"Nombre de motifs trouvés: {num_patterns}\n")
            metrics_f.write(f"Taille moyenne des motifs: {mean_length:.2f}\n")
            metrics_f.write(f"Écart type: {std_dev:.2f}\n\n")

            # Sauvegarde des motifs
            patterns_f.write(f"Support minimum: {min_support}\n")
            patterns_f.writelines(updated_patterns)
            patterns_f.write("\n")

    print("✅ L'expérience est terminée.")
