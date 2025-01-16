from itertools import combinations
from collections import defaultdict
from data_structures import Sequence, Itemset, Item

class CLOSPAN:
    def __init__(self, database, min_support):
        self.database = database
        self.min_support = min_support

    def _get_frequent_items(self, database):
        item_support = defaultdict(int)
        for sequence in database:
            unique_items = {item for itemset in sequence.itemsets for item in itemset.items}
            for item in unique_items:
                item_support[item] += 1

        return {item: count for item, count in item_support.items() if count >= self.min_support}

    def _project_database(self, database, prefix):
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

    def _count_support(self, pattern, database):
        return sum(1 for seq in database if self._is_prefix(pattern, seq))

    def _is_prefix(self, seq1, seq2):
        if len(seq1.itemsets) > len(seq2.itemsets):
            return False
        return all(seq1.itemsets[i].items.issubset(seq2.itemsets[i].items) for i in range(len(seq1.itemsets)))

    def _is_closed(self, pattern, database, support):
        for seq in database:
            if self._is_prefix(pattern, seq):
                if self._count_support(seq, database) == support:
                    return False
        return True

    def _clospan(self, database, prefix, results):
        frequent_items = self._get_frequent_items(database)

        for item, support in frequent_items.items():
            new_prefix = prefix + [Itemset({item})]
            pattern = Sequence(new_prefix)

            if self._is_closed(pattern, database, support):
                results.append((pattern, support))
                projected_db = self._project_database(database, new_prefix)
                if projected_db:
                    self._clospan(projected_db, new_prefix, results)

    def run(self):
        results = []
        self._clospan(self.database, [], results)
        return results