import os
import matplotlib.pyplot as plt
import statistics
from pathlib import Path

from config.config import DATA_PATH, DB_PATH, REPORT_PATH
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

def generate_markdown_report(limit=100, since=None, filename_graph="graph.png", filename_report="report.md", db_path=DB_PATH):
    """
    Génération d'un rapport des données enregistrées
    :param limit: Nombre maximum de données à afficher
    :param since: Date de début des données à afficher
    :param filename_graph: Nom du fichier du graphique
    :param filename_report: Nom du fichier du rapport
    :param db_path: Chemin de la base de données
    """
    if since:
        timestamps, cpu, ram, _ = storage.get_last_time_metrics(since, db_path)
    else:
        timestamps, cpu, ram, _ = storage.get_last_metrics(limit, db_path)

    if not timestamps:
        print("No data available for the given period.")
        return

    # Créer dossier de sortie
    Path(REPORT_PATH).mkdir(parents=True, exist_ok=True)
    img_path = os.path.join(REPORT_PATH, filename_graph)
    md_path = os.path.join(REPORT_PATH, filename_report)

    # Générer le graphique
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, cpu, label="CPU (%)", marker='o')
    plt.plot(timestamps, ram, label="RAM (%)", marker='s')
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.title("System Metrics")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()

    # Statistiques
    def stat_summary(label, values):
        return (
            f"**{label}**  \n"
            f"- Moyenne : {statistics.mean(values):.2f}%  \n"
            f"- Min : {min(values):.2f}%  \n"
            f"- Max : {max(values):.2f}%  \n"
        )

    cpu_stats = stat_summary("CPU", cpu)
    ram_stats = stat_summary("RAM", ram)

    # Génération du Markdown
    with open(md_path, "w") as f:
        f.write("# Rapport de performance système\n\n")
        f.write(f"**Période** : {timestamps[0]} -> {timestamps[-1]}\n\n")
        f.write("## Résumé\n\n")
        f.write(cpu_stats + "\n")
        f.write(ram_stats + "\n")
        f.write("## Graphique\n\n")
        f.write(f"![Graphique CPU/RAM]({os.path.basename(img_path)})\n")

    print(f"[✓] Rapport généré : {md_path}")