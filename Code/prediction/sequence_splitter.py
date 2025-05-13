import random

""" 
Description du script :
Ce script permet de lire des séquences à partir d'un fichier, de diviser ces séquences en
ensembles d'entraînement et de test, puis d'écrire ces ensembles dans de nouveaux fichiers.
Le script gère également le cas de fenêtre pour les tests afin de permettre une validation
croisée sur plusieurs fenêtres.
"""

def read_sequences(file_path):
    """
    Lit les séquences depuis un fichier. Chaque ligne du fichier est considérée comme une séquence.

    Args:
        file_path (str): Le chemin du fichier contenant les séquences.

    Returns:
        list: Liste des séquences lues, avec les espaces inutiles enlevés.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]  # On élimine les lignes vides


def split_sequences(sequences, train_ratio=0.8, test_window_index=0, shuffle=False, seed=42):
    """
    Divise les séquences en ensembles d'entraînement et de test selon un ratio donné et un indice de fenêtre de test.

    Args:
        sequences (list): Liste des séquences à diviser.
        train_ratio (float): Proportion des séquences utilisées pour l'entraînement (par défaut 0.8).
        test_window_index (int): Indice de la fenêtre de test (0 pour la première fenêtre, 1 pour la suivante, etc.).
        shuffle (bool): Indique si les séquences doivent être mélangées avant de les diviser.
        seed (int): La graine utilisée pour le mélanger des données si shuffle=True.

    Returns:
        tuple: Deux listes, la première pour l'ensemble d'entraînement, la seconde pour l'ensemble de test.
    """
    if shuffle:
        random.seed(seed)  # Initialiser le générateur de nombres aléatoires avec la graine donnée
        random.shuffle(sequences)  # Mélanger les séquences
    
    total = len(sequences)
    window_size = int(total * (1 - train_ratio))  # Calcul de la taille de l'ensemble de test
    
    start = test_window_index * window_size
    end = start + window_size
    
    # Cas limite : éviter de dépasser la taille des données
    if end > total:
        raise ValueError("L'indice de fenêtre dépasse la taille des données.")

    test_seqs = sequences[start:end]
    train_seqs = sequences[:start] + sequences[end:]
    
    return train_seqs, test_seqs


def write_sequences(sequences, file_path):
    """
    Écrit les séquences dans un fichier.

    Args:
        sequences (list): Liste des séquences à écrire dans le fichier.
        file_path (str): Le chemin du fichier de sortie.
    """
    with open(file_path, 'w') as f:
        for seq in sequences:
            f.write(seq + '\n')  # Écrire chaque séquence dans une nouvelle ligne du fichier


def main():
    """
    Fonction principale qui gère le flux de travail :
    - Chargement des séquences depuis un fichier.
    - Division des séquences en ensembles d'entraînement et de test.
    - Sauvegarde des ensembles dans des fichiers.
    """
    input_file = 'text_files/spmf_input.txt'  # Le fichier source contenant toutes les séquences
    train_file = 'text_files/sequence_train.txt'
    test_file = 'text_files/sequence_test.txt'

    sequences = read_sequences(input_file)  
    train_sequences, test_sequences = split_sequences(sequences,shuffle=True)  

    write_sequences(train_sequences, train_file)  
    write_sequences(test_sequences, test_file)  

    print(f"Total sequences: {len(sequences)}")
    print(f"Train: {len(train_sequences)} -> {train_file}")
    print(f"Test: {len(test_sequences)} -> {test_file}")

if __name__ == "__main__":
    main()
