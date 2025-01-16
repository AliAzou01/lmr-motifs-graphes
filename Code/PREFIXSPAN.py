from data_structures import Sequence, Itemset, Item

class PrefixSpan:
    def __init__(self, database, min_support):
        """
        Initialise l'algorithme PrefixSpan.
        :param database: Liste de séquences (instances de Sequence).
        :param min_support: Support minimum (entier).
        """
        self.database = database
        self.min_support = min_support

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

    def _prefixspan(self, database, prefix, results):

        """
        Applique PrefixSpan récursivement.
        :param database: Base projetée courante.
        :param prefix: Préfixe courant (liste d'itemsets).
        :param results: Liste des motifs fréquents trouvés.
        """
        
        frequent_items = self._get_frequent_items(database)
        
        for item, support in frequent_items.items():
    
            new_prefix = prefix + [Itemset({item})]
            results.append((Sequence(new_prefix), support))
            projected_db = self._project_database(database, new_prefix)

            if projected_db:
                self._prefixspan(projected_db, new_prefix, results)


    def run(self):
        """
        Exécute l'algorithme PrefixSpan.
        :return: Liste de tuples (motif fréquent, support).
        """
        results = []
        self._prefixspan(self.database, [], results)
        return results


