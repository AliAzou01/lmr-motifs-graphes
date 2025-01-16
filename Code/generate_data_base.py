import random
from data_structures import Sequence, Itemset, Item

def generate_large_sequence_database(num_sequences=100, max_itemsets_per_sequence=10, max_items_per_itemset=5):
    """
    Génère une grande base de données de séquences aléatoires.

    :param num_sequences: Nombre total de séquences dans la base de données.
    :param max_itemsets_per_sequence: Nombre maximal d'itemsets par séquence.
    :param max_items_per_itemset: Nombre maximal d'items par itemset.
    :return: Une base de données sous forme de liste d'objets Sequence.
    """
    
    database = []
    for _ in range(num_sequences):
        num_itemsets = random.randint(1, max_itemsets_per_sequence)  # Nombre d'itemsets dans la séquence
        sequence = []
        for _ in range(num_itemsets):
            num_items = random.randint(1, max_items_per_itemset)  # Nombre d'items dans l'itemset
            items = [Item(chr(random.randint(97, 122))) for _ in range(num_items)]  # Génération d'items 'a' à 'z'
            itemset = Itemset(items)
            sequence.append(itemset)
        database.append(Sequence(sequence))
    return database

def print_database(database):
    """
    Affiche la base de données de séquences de manière lisible.
    """
    for idx, sequence in enumerate(database):
        print(f"Sequence {idx + 1}: {sequence}")