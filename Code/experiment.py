import os
import time
from datetime import datetime
from transform import *
from baseEntier import *
from runAlgoSPMF import run_spmf
import numpy as np
from post_traitement import *



# Fonction pour calculer la taille moyenne des motifs et l'écart type
def calculate_metrics(patterns):
    lengths = [len(pattern.split(" -1")) - 1 for pattern in patterns]  # -1 sépare les éléments d'un motif
    mean_length = np.mean(lengths)
    std_dev = np.std(lengths)
    return mean_length, std_dev


# Exemple d'utilisation
if __name__ == "__main__":
    # Charger et transformer les données
    data = load_json("../Data/merged_voyages.json")
    port_to_id = map_ports_to_integers(data)
    db = transform_to_integer_database(data, port_to_id)
    write_spmf_file(db, "text_files/spmf_input_file.txt")
    spmf_input_file = "text_files/spmf_input_file.txt"

    # Créer un dictionnaire pour mapper les IDs des ports aux noms des ports
    port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

    # Valeurs de support minimum à tester
    min_supports = np.round(np.arange(0.02, 0.21, 0.01), 2)

    # Date et heure pour nommer les fichiers
    today_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Répertoire pour stocker les résultats
    os.makedirs("experiment_results", exist_ok=True)

    # Fichiers pour stocker les résultats de l'expérience
    metrics_file = f"./experiment_results/{today_datetime}_metrics.txt"
    patterns_file = f"./experiment_results/{today_datetime}_patterns.txt"

    with open(metrics_file, 'w') as metrics_f, open(patterns_file, 'w') as patterns_f:
        for min_support in min_supports:
            # Convertir le support minimum en pourcentage pour SPMF
            min_support_percentage = min_support * 100

            # Fichier de sortie pour les résultats SPMF
            spmf_output_file = "text_files/output.txt"
            output_file_filtre = "text_files/outputfiltre.txt"
            

            # Exécuter PrefixSpan via SPMF
            start_time = time.time()
            run_spmf("PrefixSpan", spmf_input_file, spmf_output_file, f"{min_support_percentage}%")
            end_time = time.time()

            # Calcul du temps en millisecondes
            prefixspan_time_ms = (end_time - start_time) * 1000

            process_results(spmf_output_file, output_file_filtre)

            # Charger les résultats générés par SPMF
            with open(output_file_filtre, 'r') as f:
                patterns = f.readlines()

            # Remplacer les IDs des ports par leurs noms
            updated_patterns = replace_ids_with_port_names(patterns, port_id_to_name)

            # Calcul des métriques
            num_patterns = len(patterns)
            mean_length, std_dev = calculate_metrics(patterns)

            # Sauvegarder les métriques
            metrics_f.write(f"Support minimum: {min_support}\n")
            metrics_f.write(f"Temps pris (ms): {prefixspan_time_ms:.2f}\n")
            metrics_f.write(f"Nombre de motifs trouvés: {num_patterns}\n")
            metrics_f.write(f"Taille moyenne des motifs: {mean_length:.2f}\n")
            metrics_f.write(f"Écart type: {std_dev:.2f}\n\n")

            # Sauvegarder les motifs trouvés
            patterns_f.write(f"Support minimum: {min_support}\n")
            patterns_f.writelines(updated_patterns)
            patterns_f.write("\n")

    print("L'expérience est terminée.")