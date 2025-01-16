import time
from GSP import *
from PREFIXSPAN import *
from generate_data_base import *
from CLOSPAN import *
from transform import *

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données JSON
    data = load_json("../Data/merged_voyages.json")

    # Transformer les données en une base de séquences
    db = transform_to_limited_database(data)

    # Paramètre de support minimal
    min_support = 200

    import time

    # PrefixSpan
    start_time = time.time()
    prefixspan = PrefixSpan(db, min_support)
    prefixspan_result = prefixspan.run()
    end_time = time.time()

    # Afficher les motifs fréquents pour PrefixSpan
    print("\nMotifs fréquents finaux (PrefixSpan):")
    for pattern, support in prefixspan_result:
        print(f"Motif: {pattern}, Support: {support}")

    # Calcul du temps en millisecondes
    prefixspan_time_ms = (end_time - start_time) * 1000
    print(f"\nTemps d'exécution PrefixSpan: {prefixspan_time_ms:.2f} ms")
