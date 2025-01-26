import numpy as np
from collections import defaultdict
from data_structures import Item, Itemset, Sequence


def replace_ids_with_port_names(patterns, port_id_to_name):
    

    updated_patterns = []


    for pattern in patterns:
        # Vérifier si le motif contient le support "#SUP:"
        if " #SUP:" in pattern:

            items = pattern.split(" #SUP:")[0].strip().split(" -1")
            named_items = []  

            for itemset in items:
                if itemset.strip(): 
                    # Remplacer chaque ID par son nom de port ou "Unknown(ID)" si non trouvé
                    item_names = [
                        port_id_to_name.get(int(item), f"Unknown({item})") 
                        for item in itemset.strip().split()
                    ]
                    # Créer une représentation en accolade pour l'ensemble d'éléments
                    named_items.append("{" + ", ".join(item_names) + "}")
            
            # Reconstituer le motif avec les noms et ajouter le support "#SUP:"
            updated_pattern = " -> ".join(named_items) + f" #SUP:{pattern.split(' #SUP:')[1]}"
            updated_patterns.append(updated_pattern)
        else:
            # Si le motif ne contient pas de support, l'ajouter tel quel
            updated_patterns.append(pattern)
    
    return updated_patterns

