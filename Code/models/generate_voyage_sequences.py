"""
generate_voyage_sequences.py

Ce script permet de générer des séquences de voyages maritimes au format SPMF à partir des données d'un navire.
- Charge les trajets (départ, arrivée, dates) pour un navire donné.
- Calcule une durée optimale de découpage des séquences.
- Transforme les voyages en séquences d'IDs de ports, séparées par des marqueurs SPMF (-1 et -2).
- Affiche les séquences brutes et nommées.

Utilisation : exécution directe via un identifiant IMO.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from models.baseEntier import load_json

# Ajout du dossier parent au chemin d'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_date(date_str):
    """Convertit une chaîne de date ISO en objet datetime."""
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

def write_spmf_file_voyage(database, file_name):
    """
    Écrit la base de données SPMF (liste de séquences d'IDs) dans un fichier texte.
    
    Args:
        database (list[list[int]]): Séquences d'IDs avec séparateurs SPMF.
        file_name (str): Nom du fichier de sortie.
    """
    with open(file_name, 'w') as file:
        for sequence in database:
            line = ' '.join(str(item) for item in sequence)
            file.write(line + "\n")

def find_optimal_duration(travel_data):
    """
    Détermine une durée de découpage optimale basée sur le plus grand écart entre durées croissantes.
    
    Args:
        travel_data (list[tuple]): Liste (departure_port, arrival_port, duration).
    
    Returns:
        float: Valeur seuil en jours si < 50.
    """
    durations = sorted([duration for _, _, duration in travel_data if duration > 0])
    
    if len(durations) < 2:
        return 10  # Durée par défaut

    max_gap = 0
    best_cutoff = durations[0]

    for i in range(1, len(durations)):
        gap = durations[i] - durations[i - 1]
        if gap > max_gap:
            max_gap = gap
            best_cutoff = durations[i]
    
    if best_cutoff > 50:
        return 50
    return best_cutoff

def load_travel_chip(identifiant, mmsi=False):
    """
    Charge les trajets d'un navire identifié par IMO ou MMSI.

    Args:
        identifiant (int): Identifiant IMO ou MMSI.
        mmsi (bool): Si True, utilise MMSI au lieu d'IMO.

    Returns:
        list[tuple]: Liste de (departure_port, arrival_port, duration)
    """
    data = load_json("../Data/merged_voyages.json")
    key = "mmsi" if mmsi else "imo"
    voyages = [v for v in data if v.get(key) == identifiant]
    voyages.sort(key=lambda v: parse_date(v["arrival_date"]))

    travel_data = []
    reference_date = datetime(2022, 1, 1)

    for v in voyages:
        departure_port = v["departure_port"] or "FICTIF"
        arrival_port = v["arrival_port"] or "FICTIF"

        departure_date = parse_date(v["departure_date"]) if departure_port != "FICTIF" else reference_date
        arrival_date = parse_date(v["arrival_date"]) if arrival_port != "FICTIF" else reference_date

        duration = (arrival_date - departure_date).total_seconds() / 86400  # en jours
        travel_data.append((departure_port, arrival_port, duration))
    
    return travel_data

def transform_to_integer_database(data, port_to_id, duree, use_duration=True):
    """
    Transforme des trajets en base SPMF avec séparateurs (-1 et -2).
    
    Args:
        data (list): (departure_port, arrival_port, duration)
        port_to_id (dict): Mapping ports → IDs.
        duree (float): Durée seuil pour couper les séquences.
        use_duration (bool): Si True, utilise la durée cumulée pour découper.
    
    Returns:
        list[list[int]]: Base de séquences au format SPMF.
    """
    database = []
    current_sequence = []
    accumulated_duration = 0
    last_port = None

    for departure_port, arrival_port, duration in data:
        departure_id = port_to_id[departure_port]
        arrival_id = port_to_id[arrival_port]

        if departure_id != last_port:
            current_sequence.append(departure_id)
            current_sequence.append(-1)
            last_port = departure_id

        if arrival_id != last_port:
            current_sequence.append(arrival_id)
            current_sequence.append(-1)
            last_port = arrival_id

        if use_duration:
            accumulated_duration += duration
            if accumulated_duration >= duree:
                current_sequence[-1] = -2  # Fin de séquence
                database.append(current_sequence)
                current_sequence = []
                accumulated_duration = 0
                last_port = None

    if current_sequence:
        current_sequence[-1] = -2
        database.append(current_sequence)

    return database

# === Programme principal ===
if __name__ == "__main__":
    while True:
        try:
            identifiant = int(input("Entrez un numéro IMO du navire : "))
            break
        except ValueError:
            print("Veuillez entrer un numéro valide (entier).")
    
    voyages = load_travel_chip(identifiant)
    optimal_duration = find_optimal_duration(voyages)

    print(f"\n--- Durée optimale calculée : {optimal_duration:.2f} jours ---")
    print("\n--- Liste des voyages ---")
    for voyage in voyages:
        print(f"Départ: {voyage[0]}, Arrivée: {voyage[1]}, Durée: {voyage[2]:.2f} jours")

    port_to_id = load_json("../Data/port_mapping.json")
    database = transform_to_integer_database(voyages, port_to_id, optimal_duration, use_duration=True)

    print("\n--- Base de données pour PrefixSpan ---")
    for seq in database:
        print(" ".join(map(str, seq)))

    id_to_port = {id_: port for port, id_ in port_to_id.items()}
    print("\n--- Séquences de voyages avec noms de ports ---")
    for seq in database:
        sequence_noms = []
        for item in seq:
            if item == -1:
                sequence_noms.append("-1")
            elif item == -2:
                sequence_noms.append("-2")
            else:
                sequence_noms.append(id_to_port[item])
        print(" ".join(sequence_noms))
