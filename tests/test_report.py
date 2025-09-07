import os
import sqlite3
import pytest

from src import report, storage
from config.config import DATA_PATH, DB_TEST_PATH, REPORT_PATH

TEST_PLOT_PATH = os.path.join(DATA_PATH, "test_report.png")
TEST_GRAPH_PATH = os.path.join(REPORT_PATH, "test_graph.png")
TEST_REPORT_PATH = os.path.join(REPORT_PATH, "test_report.md")

@pytest.fixture(autouse=True)
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

    if os.path.exists(TEST_GRAPH_PATH):
        os.remove(TEST_GRAPH_PATH)
    assert not os.path.exists(TEST_GRAPH_PATH)

    if os.path.exists(TEST_REPORT_PATH):
        os.remove(TEST_REPORT_PATH)
    assert not os.path.exists(TEST_REPORT_PATH)



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

def test_generate_report_file():
    """
    L'application doit pouvoir créer une image de rapport et un rapport non vide
    """
    report.generate_markdown_report(limit=5, filename_graph="test_graph.png", filename_report="test_report.md", db_path=DB_TEST_PATH)
    assert os.path.exists(TEST_GRAPH_PATH)
    assert os.path.exists(TEST_REPORT_PATH)
    assert os.path.getsize(TEST_GRAPH_PATH) > 0
    assert os.path.getsize(TEST_REPORT_PATH) > 0
