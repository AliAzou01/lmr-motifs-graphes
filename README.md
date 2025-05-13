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

Ce projet permet d'analyser des séquences de voyages maritimes en extrayant des motifs fréquents. Les données sont transformées en séquences numériques, puis traitées pour visualiser et analyser les relations entre les différents ports maritimes. Deux approches sont utilisées pour prédire les prochains ports d'escale : l'une basée sur les séquences complètes de trajets, l'autre sur des motifs fréquents extraits à l’aide de l’algorithme PrefixSpan. À partir de ces données, des chaînes de Markov de différents ordres sont construites pour modéliser les transitions entre ports, et la précision des prédictions est évaluée sur des ensembles d’entraînement et de test.

---

## Instructions pour Exécuter les Scripts

### 1. **Pré-requis**

Pour exécuter les différents algorithmes, il est conseillé d’avoir la version suivante de Java :

    openjdk version "21" 2023-09-19

Assurez-vous également d’avoir Python installé. Vous pouvez vérifier cela en exécutant la commande suivante dans votre terminal :

    python --version

---

### 2. **Exécution des Scripts**

Pour exécuter les différents scripts du projet, suivez les étapes ci-dessous :

1. Accédez au répertoire `Code` où tous les scripts sont situés :

    cd /chemin/vers/le/dossier/Code

2. Lancez le script souhaité avec la commande suivante :

    python3 nom_du_script.py

Par exemple, pour exécuter `mainPREFIXSPAN.py` :

    python3 main/mainPREFIXSPAN.py

---

### 3. **Visualisation des Résultats**

- **Visualisation des motifs fréquents** : ouvrez le fichier `motif_visualisation_page.html` situé dans le dossier `visualisation_motifs`. Ce fichier peut être ouvert dans un navigateur pour voir une représentation graphique des motifs extraits, avec leur support minimum et leur taille.

---

### 4. Génération du Planning pour un Navire

Pour générer un planning pour un navire spécifique, exécutez le script suivant :

    python3 planning/generate_planning.py

Lorsque le script est lancé, il vous demandera de saisir l’IMO du navire concerné.  
Un fichier de planning au format JSON sera ensuite généré automatiquement dans le dossier :

    Data/planning/

Le nom du fichier sera de la forme :

    planning_<IMO>.json


### 5. **Protocole de Prédiction des Ports (sur l'ensemble de la flotte ou un seul navire)**

Voici le protocole complet pour prédire les ports à venir à partir des séquences de trajets :

1. **Génération des séquences au format SPMF** à partir du fichier `merged_voyages.json` :

    python3 main/generate_spmf_input.py

    NB : Si vous souhaitez appliquer ce protocole sur un seul navire, exécutez `mainNavirePrefix.py` au lieu de `generate_spmf_input.py`. Cela permettra de remplir le fichier `spmf_input.txt` uniquement avec les séquences du navire spécifié. Les étapes suivantes restent identiques.

2. **Séparation des séquences** en ensembles d'entraînement et de test :

    python3 prediction/sequence_splitter.py

3. **Extraction des motifs fréquents** à partir de l’ensemble d’entraînement (la sortie doit être redirigée vers `sequences.txt`) :

    python3 main/mainPREFIXSPAN.py > text_files/sequences.txt

4. **Conversion des motifs** extraits en fichier JSON utilisable par les modèles :

    python3 prediction/motif_to_json.py

5. **Évaluation ou validation croisée** :

    - Pour la validation croisée (avec des chaînes de Markov apprises sur les motifs ou les séquences) :

        python3 prediction/cross_validation_markov_from_patterns.py

        ou

        python3 prediction/cross_validation_markov_from_sequences.py

    - Pour une évaluation simple :

        - Basée sur les motifs :

            python3 prediction/evaluate_markov_patern_multiple_orders.py

        - Basée sur les séquences :

            python3 prediction/evaluate_markov_sequence_multiple_orders.py
---

NB : Cette ligne est mise en commentaire :

    plot_transition_matrix(transition_probabilities, "matrice_transition_patern")

En effet, lorsqu’on travaille avec l’ensemble de la flotte, les matrices de transition peuvent devenir très volumineuses et coûteuses à générer. Par conséquent, cette fonction peut prendre beaucoup de temps à s'exécuter.  
Si vous avez besoin de visualiser les matrices de transition, pensez à décommenter cette ligne.

