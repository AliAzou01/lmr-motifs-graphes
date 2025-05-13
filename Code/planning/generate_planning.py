
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from datetime import datetime

with open("../Data/merged_voyages.json", "r", encoding="utf-8") as f:
    voyages = json.load(f)

imo_filter = input("Entrez l'IMO du navire que vous voulez voir : ").strip()

#  pour formater les dates
def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y %H:%M")
    return None

filtered_planning = []

for voyage in voyages:
    if str(voyage["imo"]) == imo_filter:  
        planning_entry = {
            "P2P_ID": voyage["id"],
            "VOYAGE_ID": None,
            "CARRIER_ALIAS": "Unknown Carrier",  
            "SCAC_CODE": None,
            "CARRIER_SERVICE_DES": None,
            "VESSEL_NAME": f"Vessel {voyage['imo']}",
            "VESSEL_IMO": str(voyage["imo"]),
            "VOYAGE": None,  
            "ORIGIN": voyage["departure_port"],
            "ORIGIN_PORT_CODE": voyage["departure_port"],
            "ORIGIN_TYPE_CODE": None,
            "ORIGIN_EVENTDATE": format_date(voyage["departure_date"]),
            "DESTINATION": voyage["arrival_port"],
            "DESTINATION_PORT_CODE": voyage["arrival_port"],
            "DESTINATION_TYPE_CODE": None,
            "DESTINATION_EVENTDATE": format_date(voyage["arrival_date"]),
            "ROUTING": f"{voyage['departure_port']}-{voyage['arrival_port']}",
            "MODIFIED_DATE": None,
            "AMENDMENT_CODE": None,
            "NO_OF_TRANSSHIPMENTS": None,
            "TRANSIT_TIME": (datetime.strptime(voyage["arrival_date"], "%Y-%m-%dT%H:%M:%S") - datetime.strptime(voyage["departure_date"], "%Y-%m-%dT%H:%M:%S")).days,  # durée de trajet
            "SCHEDULE_TYPE": None
        }
        
        filtered_planning.append(planning_entry)

if not filtered_planning:
    print(f" Aucun voyage trouvé pour l'IMO {imo_filter}. Vérifiez l'IMO et réessayez.")
else:
    final_json = {
        "HEADER": {
            "DATASET": "p2p_master",
            "RECORDS_RETURNED": len(filtered_planning),
            "SCHEMA_PATH": "/get/schema/p2p_master"
        },
        "DATA": filtered_planning
    }

    output_folder = "../Data/planning"
    os.makedirs(output_folder, exist_ok=True)

    output_filename = os.path.join(output_folder, f"planning_{imo_filter}.json")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4)

    print(f" Planning généré avec succès pour IMO {imo_filter} ! Fichier : {output_filename}")