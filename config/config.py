import os

# Racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin vers le dossier de données
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_PATH, "metrics.db")

DB_TEST_PATH = os.path.join(DATA_PATH, "metrics_test.db")

# Chemin vers le dossier de rapport
REPORT_PATH = os.path.join(PROJECT_ROOT, "report")