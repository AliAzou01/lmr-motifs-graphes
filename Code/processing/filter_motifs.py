"""
filter_motifs.py

Ce script lit un fichier contenant des motifs fréquents issus d’un algorithme séquentiel
(type PrefixSpan au format SPMF) et applique des filtres pour supprimer les motifs non pertinents,
par exemple :
  - motifs avec répétitions consécutives de ports,
  - motifs ne contenant qu’un seul port unique,
  - motifs avec moins de deux ports différents.

Le résultat filtré est écrit dans un fichier de sortie.
"""

def process_results(input_file, output_file):
    """
    Filtre les motifs fréquents en supprimant ceux qui ne respectent pas certains critères de qualité.

    Critères d'exclusion :
      1. Présence de ports consécutifs répétés (e.g., 5 -1 5)
      2. Moins de deux ports uniques (motif trivial ou vide)
    
    Args:
        input_file (str): Chemin vers le fichier d’entrée contenant les motifs minés (format SPMF).
        output_file (str): Chemin vers le fichier de sortie avec les motifs filtrés.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # Sauter les lignes vides

            # Séparer motif et support
            motif, _ = line.split("#SUP:")

            # Extraire les ports (IDs numériques séparés par -1)
            ports = [int(x) for x in motif.split("-1") if x.strip().isdigit()]

            # Vérifications
            unique_ports = set(ports)
            has_consecutive_repetition = any(
                ports[i] == ports[i + 1] for i in range(len(ports) - 1)
            )

            # Filtrage selon les critères
            if has_consecutive_repetition or len(unique_ports) < 2:
                continue  # Motif exclu

            # Motif valide : écrire dans le fichier de sortie
            outfile.write(line)
