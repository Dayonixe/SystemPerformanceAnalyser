# src/storage.py

import sqlite3
import os
import json

DB_PATH = os.path.join("data", "metrics.db")

def init_database():
    """
    Initialisation de la base de données
    """
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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

def insert_metrics(metrics: dict):
    """
    Insertion de données dans la base de données
    :param metrics: Dictionnaire contenant les données à insérer dans la base de données
    """
    conn = sqlite3.connect(DB_PATH)
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

def get_last_metrics(limit=5):
    """
    Récupération des dernières lignes ajoutées à la base de données
    :param limit: Nombre de ligne à récupérer
    :return: Dernières lignes ajoutées à la base de données
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, cpu, ram, top_processes
        FROM metrics
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows
