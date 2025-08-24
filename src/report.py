import os
import sqlite3
import matplotlib.pyplot as plt

from datetime import datetime
from config.config import DATA_PATH, DB_PATH

def fetch_metrics(limit=100):
    """
    Récupération des données depuis la base de données
    :param limit: Nombre maximum de données à récupérer
    :return: triplets de listes avec timestamps, cpu, et ram
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, cpu, ram FROM metrics
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    # Convertir les timestamps en objets datetime
    timestamps = [datetime.fromisoformat(r[0]) for r in reversed(rows)]
    cpu = [r[1] for r in reversed(rows)]
    ram = [r[2] for r in reversed(rows)]

    return timestamps, cpu, ram

def generate_plot(limit=100, save=False, filename="report.png"):
    """
    Génération d'un graphique des données enregistrées
    :param limit: Nombre maximum de données à afficher
    :param save: Booléen indiquant la volonté d'enregistrer le fichier
    :param filename: Nom du fichier s'il est enregistré
    """
    timestamps, cpu, ram = fetch_metrics(limit)

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