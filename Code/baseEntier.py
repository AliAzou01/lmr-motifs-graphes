from collections import defaultdict
from data_structures import Sequence , Itemset , Item
import json

# Fonction pour charger les données JSON
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Fonction pour mapper les ports à des entiers
def map_ports_to_integers(data):
    port_to_id = {}
    current_id = 1

    for voyage in data:
        departure_port = voyage.get("departure_port")
        arrival_port = voyage.get("arrival_port")
        
        if departure_port and departure_port not in port_to_id:
            port_to_id[departure_port] = current_id
            current_id += 1
        
        if arrival_port and arrival_port not in port_to_id:
            port_to_id[arrival_port] = current_id
            current_id += 1

    return port_to_id

from collections import defaultdict

def transform_to_integer_database(data, port_to_id):
    database = []
    navire_sequences = defaultdict(list)

    seen_trips = set()  # Pour garder une trace des voyages déjà ajoutés (éviter duplication)
    last_item = None  # Pour éviter d'ajouter deux fois le même port consécutivement

    for voyage in data:
        navire_id = voyage.get("imo") or voyage.get("mmsi")  # Utiliser imo ou mmsi comme identifiant unique
        if not navire_id:
            continue  # Passer au prochain voyage si aucun identifiant valide n'est trouvé

        departure_port = voyage.get("departure_port")
        arrival_port = voyage.get("arrival_port")
        arrival_date = voyage.get("arrival_date")

        # Ignorer les voyages incomplets ou mal formatés
        if not (departure_port and arrival_port and arrival_date):
            continue

        # Créer une clé unique pour ce voyage
        current_trip = (departure_port, arrival_port, arrival_date)

        # Vérifier si le voyage est déjà vu
        if current_trip in seen_trips:
            continue

        # Ajouter le port de départ si différent du dernier ajouté
        if departure_port and last_item != departure_port:
            navire_sequences[navire_id].append((arrival_date,  # Date pour trier
                                                Itemset([Item(port_to_id[departure_port])])))
            last_item = departure_port

        # Ajouter le port d'arrivée si différent du dernier ajouté
        if arrival_port and last_item != arrival_port:
            navire_sequences[navire_id].append((arrival_date,
                                                Itemset([Item(port_to_id[arrival_port])])))
            last_item = arrival_port

        # Marquer ce voyage comme vu
        seen_trips.add(current_trip)

    # Trier les séquences de chaque navire par date avant d'ajouter à la base de données
    for itemsets in navire_sequences.values():
        itemsets.sort(key=lambda x: x[0])  # Trier par la date (x[0])
        database.append(Sequence([itemset[1] for itemset in itemsets]))  # Extraire uniquement les Itemsets

    return database


# Fonction pour écrire la base dans un fichier texte SPMF
def write_spmf_file(database, file_name):
    with open(file_name, 'w') as file:
        for sequence in database:
            file.write(str(sequence) + "\n")

# Fonction pour afficher la base de données
def print_database(database):
    print("============ Database ============")
    for i, sequence in enumerate(database, start=1):
        print(f"Sequence {i}: {sequence}\n\n")
    print("==================================")



