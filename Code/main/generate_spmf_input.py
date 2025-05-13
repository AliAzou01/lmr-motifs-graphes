import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.baseEntier import *
from processing.runAlgoSPMF import *
from processing.decode_patterns import *
from processing.filter_motifs import *

if __name__ == "__main__":
    # Charger les données JSON
    data = load_json("../Data/merged_voyages.json")

    # Mapper les ports à des IDs
    port_to_id = load_json("../Data/port_mapping.json")
    db = transform_to_integer_database(data, port_to_id)

    # Créer un dictionnaire pour mapper les IDs des ports aux noms des ports
    port_id_to_name = {port_id: port_name for port_name, port_id in port_to_id.items()}

    # Fichier pour SPMF
    spmf_input_file = "text_files/spmf_input.txt"
    
    # Sauvegarder la base de données au format SPMF
    print(f"Enregistrement des données au format SPMF dans {spmf_input_file}...")
    write_spmf_file(db, spmf_input_file)
    print(f"Fichier {spmf_input_file} a été rempli avec les séquences.")
