"""
Script de transformation des données de trajets maritimes en format SPMF pour analyse de séquences.
- Lit des données JSON contenant les ports de départ et d'arrivée.
- Transforme ces trajets en une base de séquences SPMF en format entier.
- Gère les doublons et trie les événements par date pour chaque navire.
- Offre des fonctions utilitaires pour afficher ou sauvegarder la base.
"""

import json
from collections import defaultdict
from models.data_structures import Sequence, Itemset, Item

def load_json(file_path):
    """Charge un fichier JSON depuis le chemin donné."""
    with open(file_path, 'r') as file:
        return json.load(file)

def transform_to_integer_database(data, port_to_id):
    """
    Transforme des données de trajets maritimes en une base de données de séquences SPMF.
    - Utilise port_to_id pour convertir les noms de ports en IDs.
    - Évite les doublons et les ports consécutifs identiques.
    - Trie les événements par date pour chaque navire.
    
    Args:
        data (list): Liste de trajets (dictionnaires JSON).
        port_to_id (dict): Mapping des noms de ports vers des IDs entiers.

    Returns:
        list[Sequence]: Base de données SPMF prête pour l'algorithme.
    """
    database = []
    navire_sequences = defaultdict(list)
    seen_trips = set()
    last_item = None

    for voyage in data:
        navire_id = voyage.get("imo") or voyage.get("mmsi")
        if not navire_id:
            continue

        departure_port = voyage.get("departure_port")
        arrival_port = voyage.get("arrival_port")
        arrival_date = voyage.get("arrival_date")

        if not (departure_port and arrival_port and arrival_date):
            continue

        current_trip = (departure_port, arrival_port, arrival_date)
        if current_trip in seen_trips:
            continue

        if departure_port and last_item != departure_port:
            navire_sequences[navire_id].append((
                arrival_date,
                Itemset([Item(port_to_id[departure_port])])
            ))
            last_item = departure_port

        if arrival_port and last_item != arrival_port:
            navire_sequences[navire_id].append((
                arrival_date,
                Itemset([Item(port_to_id[arrival_port])])
            ))
            last_item = arrival_port

        seen_trips.add(current_trip)

    for itemsets in navire_sequences.values():
        itemsets.sort(key=lambda x: x[0])  # Trier par date
        database.append(Sequence([itemset[1] for itemset in itemsets]))

    return database

def write_spmf_file(database, file_name):
    """
    Sauvegarde la base de données SPMF dans un fichier texte.

    Args:
        database (list[Sequence]): Base de données à écrire.
        file_name (str): Nom du fichier de sortie.
    """
    with open(file_name, 'w') as file:
        for sequence in database:
            file.write(str(sequence) + "\n")

def print_database(database):
    """
    Affiche les séquences de la base en format brut (IDs).
    """
    for i, sequence in enumerate(database, start=1):
        print(sequence)

def print_database_with_names(database, port_to_id):
    """
    Affiche les séquences en remplaçant les IDs par les noms de ports.

    Args:
        database (list[Sequence]): Base de données SPMF.
        port_to_id (dict): Mapping des noms de ports vers IDs.
    """
    id_to_port = {v: k for k, v in port_to_id.items()}

    print("============ Database with Port Names ============")
    for i, sequence in enumerate(database, start=1):
        port_sequence = []
        for itemset in sequence.itemsets:
            port_names = [id_to_port[item.value] for item in itemset.items]
            port_sequence.append(f"{{{' '.join(port_names)}}}")
        print(f"Sequence {i}: {' -1 '.join(port_sequence)} -2\n")
    print("===================================================")
