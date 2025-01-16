import time
from PREFIXSPAN import PrefixSpan
from transform import load_json, transform_to_limited_database
from datetime import datetime

def run_experiment():
    # Charger les données JSON
    data = load_json("../Data/merged_voyages.json")

    # Transformer les données en une base de séquences
    db = transform_to_limited_database(data)

    # Préparer le fichier unique pour enregistrer les résultats
    current_date = datetime.now().strftime("%Y%m%d")
    output_file = f"./experiment_results/experiment_results_{current_date}.txt"

    # Écrire l'en-tête du fichier
    with open(output_file, "w") as file:
        file.write("Expérimentations de PrefixSpan\n")
        file.write(f"Date : {current_date}\n")
        file.write("Min Support | Nombre de Motifs | Taille Moyenne | Temps (ms)\n")
        file.write("-" * 50 + "\n")

    # Définir les valeurs de min_support
    min_support_values = range(100, 301, 20)

    for min_support in min_support_values:
        print(f"Exécution de PrefixSpan avec min_support = {min_support}")

        # Démarrer le chronomètre
        start_time = time.time()

        # Exécuter PrefixSpan
        prefixspan = PrefixSpan(db, min_support)
        prefixspan_result = prefixspan.run()

        # Calculer le temps pris
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000

        # Calculer les statistiques
        num_patterns = len(prefixspan_result)
        avg_pattern_length = (
            sum(len(pattern.itemsets) for pattern, _ in prefixspan_result) / num_patterns
            if num_patterns > 0
            else 0
        )

        # Ajouter les résultats au fichier
        with open(output_file, "a") as file:
            file.write(
                f"{min_support:11} | {num_patterns:15} | {avg_pattern_length:14.2f} | {execution_time_ms:10.2f}\n"
            )

        print(
            f"Min Support: {min_support}, Motifs: {num_patterns}, "
            f"Taille Moyenne: {avg_pattern_length:.2f}, Temps: {execution_time_ms:.2f} ms"
        )

    print(f"Tous les résultats ont été enregistrés dans {output_file}")

if __name__ == "__main__":
    run_experiment()
