import os
import matplotlib.pyplot as plt

from config.config import DATA_PATH, DB_PATH
from src import storage

def generate_plot(limit=100, since=None, save=False, filename="report.png", db_path=DB_PATH):
    """
    Génération d'un graphique des données enregistrées
    :param limit: Nombre maximum de données à afficher
    :param since: Date de début des données à afficher
    :param save: Booléen indiquant la volonté d'enregistrer le fichier
    :param filename: Nom du fichier s'il est enregistré
    :param db_path: Chemin de la base de données
    """
    if since:
        timestamps, cpu, ram, _ = storage.get_last_time_metrics(since, db_path)
    else:
        timestamps, cpu, ram, _ = storage.get_last_metrics(limit, db_path)

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, cpu, label="CPU Usage (%)", marker='o')
    plt.plot(timestamps, ram, label="RAM Usage (%)", marker='s')
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.title("System Metrics Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save:
        plt.savefig(os.path.join(DATA_PATH, filename))
        print(f"[✓] Report saved as {filename}")
    else:
        plt.show()