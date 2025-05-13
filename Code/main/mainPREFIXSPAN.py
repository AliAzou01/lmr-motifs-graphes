import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from models.baseEntier import *
from processing.runAlgoSPMF import *
from processing.decode_patterns import *
from processing.filter_motifs import *

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données JSON
    data = load_json("../Data/merged_voyages.json")
    

    # Mapper les ports à des IDs
    port_to_id = load_json("../Data/port_mapping.json")
    db = transform_to_integer_database(data,port_to_id)

    #print_database(db)

    # Créer un dictionnaire pour mapper les IDs des ports aux noms des ports
    port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

    while True:
        try:
            min_support = float(input("Veuillez entrer un support minimal (valeur entre 0 et 1) : "))
            if 0 < min_support <= 1:
                break
            else:
                print("Le support doit être un nombre strictement entre 0 et 1.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre décimal entre 0 et 1.")

    # Fichiers pour SPMF
    spmf_input_file = "text_files/sequence_train.txt"
    spmf_output_file = "text_files/spmf_output.txt"
    outputfiltre = "text_files/outputfiltre.txt"

    # Exécuter PrefixSpan via SPMF
    start_time = time.time()
    run_spmf("PrefixSpan", spmf_input_file, spmf_output_file, f"{min_support * 100}%")  # Convertir le support en pourcentage
    end_time = time.time()

    process_results(spmf_output_file,outputfiltre)

    # Charger les résultats générés par SPMF
    with open(outputfiltre, 'r') as f:
        patterns = f.readlines()
    

    # Remplacer les IDs des ports par leurs noms
    updated_patterns = replace_ids_with_port_names(patterns, port_id_to_name)

    # Afficher les motifs fréquents pour PrefixSpan avec noms des ports
    print("\nMotifs fréquents finaux (PrefixSpan via SPMF):")
    for pattern in updated_patterns:
        print(pattern.strip())

    # Calcul du temps en millisecondes
    spmf_time_ms = (end_time - start_time) * 1000
    print(f"\nTemps d'exécution PrefixSpan (via SPMF): {spmf_time_ms:.2f} ms")
    print("Nombre de motifs :", len(updated_patterns))
