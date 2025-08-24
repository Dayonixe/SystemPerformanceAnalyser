import os
import sqlite3
import pytest

from src import report, storage
from config.config import DATA_PATH, DB_TEST_PATH

TEST_PLOT_PATH = os.path.join(DATA_PATH, "test_report.png")

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    ###########################################################
    #                          SETUP                          #
    ###########################################################
    print("\n[SETUP] Initialisation avant les tests du module")
    os.makedirs(DATA_PATH, exist_ok=True)
    conn = sqlite3.connect(DB_TEST_PATH)
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
    # Insertion de lignes factices
    from datetime import datetime, timedelta
    now = datetime.now()
    for i in range(10):
        ts = (now - timedelta(seconds=i * 60)).isoformat()
        cursor.execute("""
            INSERT INTO metrics (timestamp, cpu, ram, top_processes)
            VALUES (?, ?, ?, ?)
        """, (ts, 50 + i, 60 + i, "[]"))
    conn.commit()
    conn.close()
    assert os.path.exists(DB_TEST_PATH)

    yield  # Exécution des tests

    ###########################################################
    #                         TEARDOWN                        #
    ###########################################################
    print("\n[TEARDOWN] Nettoyage après les tests du module")
    storage.delete_database(DB_TEST_PATH)
    assert not os.path.exists(DB_TEST_PATH)

    if os.path.exists(TEST_PLOT_PATH):
        os.remove(TEST_PLOT_PATH)
    assert not os.path.exists(TEST_PLOT_PATH)



def test_fetch_metrics_structure():
    """
    L'application doit pouvoir récupérer le triplet de liste de la base de données
    """
    timestamps, cpu, ram = report.fetch_metrics(limit=5, db_path=DB_TEST_PATH)
    assert len(timestamps) == len(cpu) == len(ram)
    assert all(isinstance(t, object) for t in timestamps)
    assert all(isinstance(c, (float, int)) for c in cpu)
    assert all(isinstance(r, (float, int)) for r in ram)

def test_generate_plot_file_saving():
    """
    L'application doit pouvoir créer une image de rapport non vide
    """
    report.generate_plot(limit=5, save=True, filename="test_report.png", db_path=DB_TEST_PATH)
    assert os.path.exists(TEST_PLOT_PATH)
    assert os.path.getsize(TEST_PLOT_PATH) > 0

def test_generate_plot_no_crash_on_display():
    """
    L'application doit pouvoir faire l'affichage du rapport sans crash
    """
    try:
        report.generate_plot(limit=5, save=False, db_path=DB_TEST_PATH)
    except Exception as e:
        pytest.fail(f"generate_plot failed when display was requested: {e}")
