import json
from collections import defaultdict
from data_structures import Item, Itemset, Sequence
from generate_data_base import *
import time
from GSP import *
from PREFIXSPAN import *
from CLOSPAN import *
import matplotlib.pyplot as plt


# Fonction pour charger les données JSON
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def transform_to_limited_database(data):
    database = []
    navire_sequences = defaultdict(list)

    for voyage in data:
        
        navire_id = voyage.get("imo")
        if not navire_id:
            continue

        # Filtrer les items invalides (ports manquants ou date absente)
        if not (voyage.get("departure_port") and voyage.get("arrival_port") and voyage.get("arrival_date")) \
            or (voyage.get("departure_port") == voyage.get("arrival_port")):
            continue

        items = [
            Item(voyage['departure_port']),
            Item(voyage['arrival_port']),
        ]

        # Ajouter l'itemset au navire correspondant
        navire_sequences[navire_id].append(Itemset(items))

    # Transformer les séquences de chaque navire en objets Sequence et trier les dates
    for itemsets in navire_sequences.values():
        database.append(Sequence(itemsets))
       

    return database

# Fonction pour afficher la base de données
def print_database(database):
    for i, sequence in enumerate(database, start=1):
        print(f"Sequence {i}: {sequence}\n\n")


# Fonction pour afficher la base de données dans un fichier texte
def write_database_to_file(database, file_name):
    with open(file_name, 'w') as file:
        for i, sequence in enumerate(database, start=1):
            file.write(f"Sequence {i}: {sequence}\n")

  
