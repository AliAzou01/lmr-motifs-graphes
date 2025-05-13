"""
generate_port_mapping.py

Ce script génère un dictionnaire associant chaque port unique (départ ou arrivée) à un identifiant entier.
Il réserve l'ID 1 pour le port fictif ("FICTIF") utilisé lorsque les données sont manquantes.
Le mapping est sauvegardé dans un fichier JSON.

Usage :
    À exécuter directement pour produire `port_mapping.json` à partir de `merged_voyages.json`.
"""

import os
import sys
import json

# Ajouter le dossier parent au path pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.baseEntier import load_json

def map_ports_to_integers(data):
    """
    Génère un mapping {nom_du_port: identifiant_entier}.

    Args:
        data (list): Liste des voyages (dictionnaires contenant departure_port et arrival_port).

    Returns:
        dict: Mapping des noms de ports vers des entiers.
    """
    port_to_id = {"FICTIF": 1}  # ID réservé pour ports fictifs
    current_id = 2  # Démarrage à 2 pour les ports réels

    for voyage in data:
        departure_port = voyage.get("departure_port")
        arrival_port = voyage.get("arrival_port")

        # Ajoute les ports s'ils ne sont pas encore mappés
        if departure_port and departure_port not in port_to_id:
            port_to_id[departure_port] = current_id
            current_id += 1
        if arrival_port and arrival_port not in port_to_id:
            port_to_id[arrival_port] = current_id
            current_id += 1

    return port_to_id

def save_json(data, file_path):
    """
    Sauvegarde un dictionnaire en fichier JSON.

    Args:
        data (dict): Données à sauvegarder.
        file_path (str): Chemin du fichier de sortie.
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# === Point d'entrée principal ===
if __name__ == "__main__":
    raw_data = load_json("../Data/merged_voyages.json")
    port_to_id = map_ports_to_integers(raw_data)
    save_json(port_to_id, "port_mapping.json")
    print("✅ Mapping sauvegardé dans 'port_mapping.json'")
