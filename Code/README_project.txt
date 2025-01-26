-----------------------------------------------------------------------
    README Projet Annuel 
-----------------------------------------------------------------------


* Ce projet est réalisé par : 
 ________________________________________________
| Nom         | Prénom      | Numéro d'étudiant  |
|-------------|-------------|--------------------|
| DJEHA       | Wassim      | 22208244           |
| KACED       | Louheb      | 22111744           |
| HALIT       | Rafik       | 22210612           |
| OULMAHDI    | Riad        | 22212014           |
| AZOU        | Ali         | 22212179           |
| KHEYAR      | Aya         | 22309669           |
|_____________|_____________|____________________|



------------------------------------------------------------------------




Ce projet permet d'analyser des séquences de voyages maritimes en extrayant des motifs fréquents. Les données sont transformées en séquences numériques, puis traitées pour visualiser et analyser les relations entre les différents ports maritimes.

### 1. **`baseEntier.py`**
Ce script transforme les données brutes en séquences SPMF (avec des entiers) prêtes à être utilisées pour l'analyse séquentielle.

### 2. **`experiment.py`**
Automatise l'extraction des motifs séquentiels, en partant des données brutes jusqu'à l'analyse et la sauvegarde des résultats expérimentaux. Ce script génère plusieurs fichiers de sortie :
- **`output.txt`** : Contient les motifs bruts extraits par l'algorithme PrefixSpan avant traitement.
- **`outputfiltre.txt`** : Contient les motifs extraits après filtration par la fonction `process_results`.
- **`Metrics File`** : Contient les métriques calculées pour chaque valeur de support minimum.
- **`Patterns File`** : Contient les motifs extraits pour chaque valeur de support minimum.

### 3. **`graph.py`**
Ce script lit une séquence de connexions entre ports (dans le fichier `sequences_from_to.txt`), extrait les relations de départ-arrivée, et les visualise sous forme de graphe. Les nœuds sont colorés pour mieux représenter les connexions entre les ports. Le fichier prend un paramètre : le numéro de la séquence à analyser. Exemple d'exécution :

```bash
python3 graph.py 5
```

### 4. **`process_results.py`**
Ce script filtre les motifs de séquences en lisant un fichier d'entrée contenant des motifs. Les motifs avec des répétitions consécutives ou ceux ayant moins de 2 ports différents sont exclus. Les motifs valides sont ensuite enregistrés dans un fichier de sortie.

### 5. **`transform.py`**
Transforme les identifiants numériques des ports dans les motifs de séquences en leurs noms correspondants, en utilisant un dictionnaire de correspondance. Cela permet d'améliorer la lisibilité des résultats.

### 6. **Visualisation des Motifs**
Pour visualiser les motifs fréquents en fonction du support minimum et de la taille des motifs, il est nécessaire de lancer le fichier HTML `motif_visualisation_page.html` situé dans le dossier `visualisation_motifs`.

### 7. **Fichiers d'Entrée et de Sortie**
- **`sequences_from_to.txt`** : Contient les connexions entre ports maritimes, utilisées pour la visualisation dans `graph.py`.
- **`output.txt`, `outputfiltre.txt`, `Metrics File`, `Patterns File`** : Fichiers générés par `experiment.py` et traités dans `process_results.py`.

---

## Instructions pour Exécuter les Scripts

### 1. **Pré-requis**

Afin de pouvoir éxecuter les différents algorithmes il est conseillé d'avoir cette version de java

openjdk version "21" 2023-09-19

Assurez-vous d'avoir Python installé. Vous pouvez vérifier cela en exécutant la commande suivante dans votre terminal :

```bash
python --version
```

### 2. **Exécution des Scripts**
Pour exécuter les différents scripts de notre projet, suivez les étapes ci-dessous :
1. Accédez au répertoire `Code` où tous les scripts sont situés :

   ```bash
   cd /chemin/vers/le/dossier/Code
   ```

2. Lancez le script voulu avec la commande suivante :

   ```bash
   python nom_du_script.py
   ```
   Par exemple, pour exécuter `graph.py` avec le paramètre de la séquence numéro 5 :
   
   ```bash
   python graph.py 5
   ```

### 3. **Visualisation des Résultats**
- **Visualisation des motifs fréquents** : Lancez `motif_visualisation_page.html` qui se trouve dans le dossier `visualisation_motifs`. Vous pouvez ouvrir ce fichier dans un navigateur pour voir la représentation graphique des motifs extraits et leur relation avec les supports minimum et les tailles des motifs.


