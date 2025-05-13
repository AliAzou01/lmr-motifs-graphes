"""
decode_patterns.py

Ce module contient une fonction utilitaire pour convertir des motifs (patterns)
minés à partir de séquences numériques (IDs de ports) en une version lisible,
où chaque ID est remplacé par le nom du port correspondant.

Typiquement utilisé pour post-traiter les résultats d’un algorithme de type PrefixSpan.
"""

def replace_ids_with_port_names(patterns, port_id_to_name):
    """
    Convertit une liste de motifs contenant des IDs de ports en motifs lisibles avec noms de ports.

    Args:
        patterns (list of str): Motifs au format SPMF contenant des IDs (avec séparateurs -1 et #SUP).
        port_id_to_name (dict): Dictionnaire {ID: nom_du_port}.

    Returns:
        list of str: Motifs lisibles avec noms de ports.
    """
    updated_patterns = []

    for pattern in patterns:
        # Traitement uniquement si le motif contient le support
        if " #SUP:" in pattern:
            # Séparation des itemsets
            items = pattern.split(" #SUP:")[0].strip().split(" -1")
            named_items = []  

            for itemset in items:
                if itemset.strip(): 
                    # Remplacement de chaque ID par son nom ou "Unknown(ID)" si manquant
                    item_names = [
                        port_id_to_name.get(int(item), f"Unknown({item})") 
                        for item in itemset.strip().split()
                    ]
                    # Formatage de l’itemset lisible
                    named_items.append("{" + ", ".join(item_names) + "}")
            
            # Reconstruction du motif lisible
            support = pattern.split(" #SUP:")[1]
            updated_pattern = " -> ".join(named_items) + f" #SUP:{support}"
            updated_patterns.append(updated_pattern)
        else:
            # Si pas de support, laisser tel quel
            updated_patterns.append(pattern)
    
    return updated_patterns
