import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from models.baseEntier import *
from processing.runAlgoSPMF import *
from Code.processing.decode_patterns import *
from Code.processing.filter_motifs import *

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données JSON
    data = load_json("../Data/merged_voyages.json")

    # Mapper les ports à des IDs
    port_to_id = load_json("../Data/port_mapping.json")
    db = transform_to_integer_database(data, port_to_id)

    # Créer un dictionnaire pour mapper les IDs des ports aux noms des ports
    port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

    # Paramètre de support minimal (entre 0 et 1)
    min_support = 0.1

    # Fichiers pour SPMF
    spmf_input_file = "text_files/spmf_input.txt"
    spmf_output_file = "text_files/spmf_output.txt"
    outputfiltre = "text_files/outputfiltre.txt"

    # Sauvegarder la base de données au format SPMF
    write_spmf_file(db, spmf_input_file)

    # Exécuter CLOSPAN via SPMF
    start_time = time.time()
    run_spmf("CloSpan", spmf_input_file, spmf_output_file, f"{min_support * 100}%")
    end_time = time.time()

    process_results(spmf_output_file,outputfiltre)

    # Charger les résultats générés par SPMF
    with open(outputfiltre, 'r') as f:
        patterns = f.readlines()

    # Remplacer les IDs des ports par leurs noms
    updated_patterns = replace_ids_with_port_names(patterns, port_id_to_name)

    # Afficher les motifs fréquents pour CLOSPAN avec noms des ports
    print("\nMotifs fréquents finaux (CLOSPAN via SPMF):")
    for pattern in updated_patterns:
        print(pattern.strip())

    # Calcul du temps en millisecondes
    spmf_time_ms = (end_time - start_time) * 1000
    print(f"\nTemps d'exécution CLOSPAN (via SPMF): {spmf_time_ms:.2f} ms")
    print("Nombre de motifs :", len(updated_patterns))
