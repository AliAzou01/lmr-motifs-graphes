
from collections import defaultdict
from transform import load_json

# Classes pour modéliser les données
class Item:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Itemset:
    def __init__(self, items):
        self.items = items

    def __str__(self):
        return " ".join(str(item) for item in self.items)

class Sequence:
    def __init__(self, itemsets):
        self.itemsets = itemsets

    def __str__(self):
        return " -1 ".join(str(itemset) for itemset in self.itemsets) + " -2"

# Fonction pour transformer les données JSON en séquences SPMF
def transform_to_spmf_database(data):
    database = []
    navire_sequences = defaultdict(list)  # Grouper par navire (imo)

    for voyage in data:
        navire_id = voyage.get("imo")
        if not navire_id:
            continue

        # Filtrer les items invalides
        if not (voyage.get("departure_port") and voyage.get("arrival_port") and voyage.get("arrival_date")) \
            or (voyage.get("departure_port") == voyage.get("arrival_port")):
            continue

        items = [
            Item(voyage['departure_port']),
            Item(voyage['arrival_port']),
        ]

        navire_sequences[navire_id].append(Itemset(items))

    # Transformer les séquences de chaque navire en objets Sequence
    for itemsets in navire_sequences.values():
        database.append(Sequence(itemsets))

    return database[:50]

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


# Exemple d'utilisation
if __name__ == "__main__":
    # Charger vos données JSON
    data = load_json("../Data/merged_voyages.json")
    # Transformer en format SPMF
    spmf_database = transform_to_spmf_database(data)

    #print_database(spmf_database)

    write_spmf_file(spmf_database, "/home/wassim/M1/spmf/src/ca/pfv/spmf/test/spmf_database.txt")