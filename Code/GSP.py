from itertools import permutations
from data_structures import Sequence, Itemset, Item

class GSP:
    def __init__(self, database, min_support):
        """
        Initialisation de l'algorithme GSP.
        :param database: Liste d'objets Sequence.
        :param min_support: Support minimum pour qu'une séquence soit fréquente.
        """
        self.database = database
        self.min_support = min_support
        self.frequent_patterns = []

    def count_support(self, candidates):
        """
        Compte le support de chaque candidat dans les séquences.
        :param candidates: Liste de séquences candidates.
        :return: Liste de tuples (candidat, support).
        """
        support_count = {tuple(candidate): 0 for candidate in candidates}
        for sequence in self.database:
            for candidate in candidates:
                if self.is_subsequence(candidate, sequence):
                    support_count[tuple(candidate)] += 1
        return [(list(candidate), count) for candidate, count in support_count.items() if count >= self.min_support]

    @staticmethod
    def is_subsequence(subseq, seq):
        """
        Vérifie si une sous-séquence est incluse dans une séquence.
        :param subseq: Sous-séquence à vérifier.
        :param seq: Séquence principale.
        :return: True si subseq est une sous-séquence de seq, sinon False.
        """
        seq_iter = iter(seq.itemsets)
        return all(any(itemset.items.issubset(s.items) for s in seq_iter) for itemset in subseq)

    def generate_candidates(self, frequent_patterns):
        """
        Génère les candidats de la prochaine longueur.
        :param frequent_patterns: Liste des motifs fréquents actuels.
        :return: Liste de nouveaux candidats.
        """
        candidates = []
        for seq1, seq2 in permutations(frequent_patterns, 2):

            
            # Récupérer le premier item de seq1 et le dernier item de seq2
            first_item = next(iter(seq1[0].items))
            last_item = next(iter(seq2[-1].items))
            
            # Supprimer first_item de seq1 et last_item de seq2
            modified_seq1 = seq1[:]
            modified_seq1[0] = Itemset(seq1[0].items - {first_item}) if seq1[0].items - {first_item} else None
           
            modified_seq2 = seq2[:]
            modified_seq2[-1] = Itemset(seq2[-1].items - {last_item}) if seq2[-1].items - {last_item} else None  
            
            # Comparer les séquences modifiées
            if modified_seq1[1:] == modified_seq2[:-1]:
                
                new_candidate = seq1 + [seq2[-1]]
                candidates.append(new_candidate)
            

            candidates = [candidate for candidate in candidates if all(len(itemset.items) > 0 for itemset in candidate)]

        return candidates


    def run(self):
        """
        Exécute l'algorithme GSP.
        :return: Liste des motifs fréquents avec leurs supports.
        """
        # Génération initiale des candidats de taille 1
        items = {item for sequence in self.database for itemset in sequence.itemsets for item in itemset.items}
        candidates = [[Itemset([item])] for item in sorted(items, key=lambda x: x.value)]  # Tri des items pour cohérence

        k = 1
        while candidates:
            
            frequent_k = self.count_support(candidates)
            if not frequent_k:
                break
            
            self.frequent_patterns.extend(frequent_k)
            candidates = self.generate_candidates([pattern for pattern, _ in frequent_k])
            k += 1
        return self.frequent_patterns
