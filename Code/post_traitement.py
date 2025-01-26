

def process_results(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue

            # Récupérer le motif (avant #SUP)
            motif, _ = line.split("#SUP:")

            # Extraire les ports (les entiers positifs séparés par -1)
            ports = [int(x) for x in motif.split("-1") if x.strip().isdigit()]

            # Vérifier les conditions d'exclusion
            unique_ports = set(ports)
            has_consecutive_repetition = any(ports[i] == ports[i + 1] for i in range(len(ports) - 1))

            # Exclusion des motifs selon les conditions :
            # 1. Si un port est répété consécutivement
            # 2. Si un seul port unique est présent
            # 3. Si moins de 3 ports différents sont présents
            if has_consecutive_repetition or len(unique_ports) < 2:
                continue

            # Si le motif passe les filtres, on l'écrit dans le fichier de sortie
            outfile.write(line)
