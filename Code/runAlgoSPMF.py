import os

# Fonction pour exécuter SPMF et retourner le fichier de sortie
def run_spmf(algorithm, input_file, output_file, parameters):
    command = f"java -jar spmf.jar run {algorithm} {input_file} {output_file} {parameters}"
    os.system(command)
    
