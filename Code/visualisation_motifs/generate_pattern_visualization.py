# Ce script permet de lire un fichier contenant des motifs fréquents générés par un algorithme d'extraction de motifs fréquents, 
# de les regrouper par taille et par min_support, et de visualiser les résultats sous forme de graphiques interactifs. 

# Pour chaque valeur de support minimum spécifiée, un graphique HTML est généré avec un menu déroulant permettant de 
# sélectionner la taille des motifs. Ce fichier peut être utilisé pour analyser visuellement les motifs extraits.

import re
import plotly.graph_objects as go

# Fonction pour lire et extraire les motifs et supports depuis le fichier texte pour un min_support donné
def load_patterns_for_support(file_path, target_min_support):
    grouped_results_by_size = {}

    with open(file_path, 'r') as file:
        current_min_support = None
        for line in file:
            # Vérifier si la ligne contient un nouveau min_support
            match_min_support = re.match(r"Support minimum:\s*([\d.]+)", line)
            if match_min_support:
                current_min_support = float(match_min_support.group(1))
                continue

            # S'assurer qu'on traite uniquement le min_support cible
            if current_min_support != target_min_support:
                continue

            # Vérifier si la ligne contient un motif et un support
            match_pattern = re.match(r"{(.+?)}( -> {.+?})* #SUP:\s*(\d+)", line)
            if match_pattern:
                pattern = match_pattern.group(0).split("#SUP:")[0].strip()  # Extraire le motif complet
                support = int(match_pattern.group(3))  # Extraire le support
                size = pattern.count("->") + 1  # Calculer la taille du motif

                # Ajouter les données au dictionnaire
                if size not in grouped_results_by_size:
                    grouped_results_by_size[size] = {
                        "patterns": [],
                        "supports": []
                    }

                grouped_results_by_size[size]["patterns"].append(pattern)
                grouped_results_by_size[size]["supports"].append(support)

    return grouped_results_by_size


def visualize_results_by_size(grouped_results_by_size, target_min_support):
    fig = go.Figure()

    # Ajouter une trace pour chaque taille de motif
    for size, group in sorted(grouped_results_by_size.items()):
        fig.add_trace(
            go.Bar(
                x=group["supports"],
                y=group["patterns"],
                orientation='h',
                name=f"Taille {size}",
                visible=(size == 2),  
            )
        )

    # Créer les boutons pour le menu déroulant
    dropdown_buttons = [
        {
            "label": f"Taille {size}",
            "method": "update",
            "args": [
                {
                    "visible": [(trace.name == f"Taille {size}") for trace in fig.data],
                },
                {"title": f"Motifs fréquents - Taille {size} (Min support {target_min_support})"},
            ],
        }
        for size in sorted(grouped_results_by_size.keys())
    ]

    # Ajouter les options et le menu déroulant au graphique
    fig.update_layout(
        title=f"Motifs fréquents - Min support {target_min_support}",
        xaxis_title="Support",
        yaxis_title="Motifs",
        yaxis=dict(automargin=True),
        updatemenus=[
            {
                "buttons": dropdown_buttons,
                "direction": "down",
                "showactive": True,
                "x": 0.5,
                "y": 1.2,
                "xanchor": "center",
                "yanchor": "top",
            }
        ],
    )

    # Sauvegarder le graphique dans un fichier HTML pour le min_support donné
    file_name = f"min_support_{str(target_min_support).replace('.', '_')}.html"
    fig.write_html(file_name)
    print(f"Le fichier '{file_name}' a été créé.")

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les motifs et générer un fichier par min_support
    file_path = "experiment_min_support.txt"
    min_supports_to_visualize = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15]  # Liste des min_support à visualiser

    for min_support in min_supports_to_visualize:
        grouped_results_by_size = load_patterns_for_support(file_path, min_support)
        visualize_results_by_size(grouped_results_by_size, min_support)
