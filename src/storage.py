import sqlite3
import os
import json
from datetime import datetime

from config.config import DATA_PATH, DB_PATH

def init_database(db_path=DB_PATH):
    """
    Initialisation de la base de données
    :param db_path: Chemin de la base de données
    """
    os.makedirs(DATA_PATH, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu REAL NOT NULL,
            ram REAL NOT NULL,
            top_processes TEXT
        )
    """)
    conn.commit()
    conn.close()

def delete_database(db_path=DB_PATH):
    """
    Suppression de la base de données
    :param db_path: Chemin de la base de données
    """
    if os.path.exists(db_path):
        os.remove(db_path)

def insert_metrics(metrics: dict, db_path=DB_PATH):
    """
    Insertion de données dans la base de données
    :param metrics: Dictionnaire contenant les données à insérer dans la base de données
    :param db_path: Chemin de la base de données
    """
    # Vérification de la donnée timestamp
    try:
        datetime.fromisoformat(metrics['timestamp'])
    except ValueError:
        raise TypeError("timestamp must be an ISO format datetime string")

    # Vérification de la donnée cpu
    if not isinstance(metrics['cpu'], (int, float)):
        raise TypeError("cpu must be a float")

    # Vérification de la donnée ram
    if not isinstance(metrics['ram'], (int, float)):
        raise TypeError("ram must be a float")

    # Vérification de la donnée top_processes
    if not isinstance(metrics['top_processes'], list):
        raise TypeError("top_processes must be a list")

    # Insertion des données dans la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO metrics (timestamp, cpu, ram, top_processes)
        VALUES (?, ?, ?, ?)
    """, (
        metrics['timestamp'],
        metrics['cpu'],
        metrics['ram'],
        json.dumps(metrics['top_processes'])  # on stocke les processus en JSON
    ))

    conn.commit()
    conn.close()

def get_last_metrics(limit=5, db_path=DB_PATH):
    """
    Récupération des dernières lignes ajoutées à la base de données
    :param limit: Nombre de ligne à récupérer
    :param db_path: Chemin de la base de données
    :return: Quadruplets de listes avec timestamps, cpu, ram, et top_processes
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, cpu, ram, top_processes
        FROM metrics
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    # Assurer une sortie toujours cohérente
    if not rows:
        return [], [], [], []

    # Extraction des données de rows
    timestamps = [datetime.fromisoformat(r[0]) for r in rows]
    cpu = [r[1] for r in rows]
    ram = [r[2] for r in rows]
    top_processes = [r[3] for r in rows]

    return timestamps, cpu, ram, top_processes

def get_last_time_metrics(since: datetime, db_path=DB_PATH):
    """
    Récupération des lignes à partir d'une date donnée
    :param since: Date de début de récupération
    :param db_path: Chemin de la base de données
    :return: Quadruplets de listes avec timestamps, cpu, ram, et top_processes
    """
    # Vérification de la donnée top_processes
    if since is None:
        raise ValueError("Le paramètre 'since' ne peut pas être None")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, cpu, ram, top_processes
        FROM metrics
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """, (since.isoformat(),))
    rows = cursor.fetchall()
    conn.close()

    # Assurer une sortie toujours cohérente
    if not rows:
        return [], [], [], []

    # Extraction des données de rows
    timestamps = [datetime.fromisoformat(r[0]) for r in rows]
    cpu = [r[1] for r in rows]
    ram = [r[2] for r in rows]
    top_processes = [r[3] for r in rows]

    return timestamps, cpu, ram, top_processes