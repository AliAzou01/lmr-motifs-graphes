import time
from models.baseEntier import *
from processing.runAlgoSPMF import *
from processing.decode_patterns import *
from processing.filter_motifs import *

def run_prefixspan(
    port_id_to_name,
    min_support=0.02,
    spmf_input_file="text_files/sequence_train.txt",
    spmf_output_file="text_files/spmf_output.txt",
    outputfiltre="text_files/outputfiltre.txt"
):
    
    # Exécuter PrefixSpan via SPMF
    start_time = time.time()
    run_spmf("PrefixSpan", spmf_input_file, spmf_output_file, f"{min_support * 100}%")
    end_time = time.time()

    # Post-traitement
    process_results(spmf_output_file, outputfiltre)

    # Charger les résultats filtrés
    with open(outputfiltre, 'r') as f:
        patterns = f.readlines()

    # Remplacer les IDs des ports par leurs noms
    updated_patterns = replace_ids_with_port_names(patterns, port_id_to_name)
    
    # Sauvegarder les motifs mis à jour dans un fichier sequences.txt
    with open("text_files/sequences.txt", "w", encoding="utf-8") as f:
        for pattern in updated_patterns:
            f.write(pattern.strip() + "\n")

    spmf_time_ms = (end_time - start_time) * 1000
    print(f"\nTemps d'exécution PrefixSpan (via SPMF): {spmf_time_ms:.2f} ms")
    print("Nombre de motifs :", len(updated_patterns))

    return updated_patterns, spmf_time_ms
