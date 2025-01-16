from concurrent.futures import ThreadPoolExecutor
from data_structures import Sequence, Itemset

class PrefixSpanParallel:
    def __init__(self, database, min_support, max_threads=4):
        """
        Initialise l'algorithme PrefixSpan parallèle.
        :param database: Liste de séquences (instances de Sequence).
        :param min_support: Support minimum (entier).
        :param max_threads: Nombre maximum de threads.
        """
        self.database = database
        self.min_support = min_support
        self.max_threads = max_threads

    def _get_frequent_items(self, database):
        """
        Trouve les items fréquents dans la base donnée.
        :param database: Liste de séquences.
        :return: Liste de tuples (item, support).
        """
        item_support = {}
        for sequence in database:
            unique_items = {item for itemset in sequence.itemsets for item in itemset.items}
            for item in unique_items:
                item_support[item] = item_support.get(item, 0) + 1

        # Filtrer les items selon le support minimum
        return {item: count for item, count in item_support.items() if count >= self.min_support}

    def _project_database(self, database, prefix):
        """
        Projette la base de données selon un préfixe donné.
        :param database: Liste de séquences.
        :param prefix: Préfixe courant (liste d'itemsets).
        :return: Base projetée.
        """
        projected_db = []
        for sequence in database:
            suffix_itemsets = []
            found_prefix = False
            for itemset in sequence.itemsets:
                if found_prefix:
                    suffix_itemsets.append(itemset)
                elif prefix[-1].items.issubset(itemset.items):
                    found_prefix = True
                    suffix_itemset = Itemset(itemset.items - prefix[-1].items)
                    if suffix_itemset.items:
                        suffix_itemsets.append(suffix_itemset)
            if found_prefix and suffix_itemsets:
                projected_db.append(Sequence(suffix_itemsets))
        return projected_db

    def _prefixspan_worker(self, database, prefix):
        """
        Fonction pour exécuter une branche du PrefixSpan.
        :param database: Base projetée courante.
        :param prefix: Préfixe courant (liste d'itemsets).
        :return: Résultats partiels (liste de tuples (motif fréquent, support)).
        """
        results = []
        frequent_items = self._get_frequent_items(database)
        for item, support in frequent_items.items():
            new_prefix = prefix + [Itemset({item})]
            results.append((Sequence(new_prefix), support))
            projected_db = self._project_database(database, new_prefix)
            if projected_db:
                # Appel récursif pour continuer l'exploration
                results.extend(self._prefixspan_worker(projected_db, new_prefix))
        return results

    def run(self):
        """
        Exécute l'algorithme PrefixSpan en parallèle.
        :return: Liste de tuples (motif fréquent, support).
        """
        results = []
        frequent_items = self._get_frequent_items(self.database)

        # Préparation des tâches pour les threads
        tasks = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for item, support in frequent_items.items():
                prefix = [Itemset({item})]
                projected_db = self._project_database(self.database, prefix)
                if projected_db:
                    # Soumettre une tâche pour chaque préfixe initial
                    tasks.append(executor.submit(self._prefixspan_worker, projected_db, prefix))

            # Récupérer les résultats
            for task in tasks:
                results.extend(task.result())

        # Ajouter les préfixes initiaux aux résultats
        for item, support in frequent_items.items():
            results.append((Sequence([Itemset({item})]), support))

        return results
