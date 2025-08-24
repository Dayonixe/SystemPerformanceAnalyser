import os

# Chemin vers le dossier de données (relatif à la racine du projet)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_PATH, "metrics.db")