import pytest
import sqlite3
import os
import json

from src import collector, storage
from config.config import DB_TEST_PATH

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    ###########################################################
    #                          SETUP                          #
    ###########################################################
    print("\n[SETUP] Initialisation avant les tests du module")
    storage.init_database(DB_TEST_PATH)
    assert os.path.exists(DB_TEST_PATH)

    yield  # Exécution des tests

    ###########################################################
    #                         TEARDOWN                        #
    ###########################################################
    print("\n[TEARDOWN] Nettoyage après les tests du module")
    storage.delete_database(DB_TEST_PATH)
    assert not os.path.exists(DB_TEST_PATH)



def test_init_database_creates_file_and_table():
    """
    L'application doit pouvoir créer le fichier de base de données et la table 'metrics'
    """
    conn = sqlite3.connect(DB_TEST_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics';")
    assert cursor.fetchone() is not None
    conn.close()

def test_storage_insert_and_read():
    """
    L'application doit pouvoir initier la base de données au besoin, ajouter et lire des données dans la base de données
    """
    data = collector.collect_metrics()
    storage.insert_metrics(data)

    rows = storage.get_last_metrics(limit=1)
    assert len(rows) == 1
    ts, cpu, ram, processes = rows[0]

    assert isinstance(ts, str)

    assert isinstance(cpu, float)
    assert isinstance(ram, float)

    proc_list = json.loads(processes)
    assert isinstance(proc_list, list)
    assert all('pid' in p and 'name' in p and 'cpu_percent' in p for p in proc_list)

def test_insert_and_read_manual_data():
    """
    L'application doit pouvoir insérer des données manuellement et les relire correctement
    """
    mock_data = {
        'timestamp': '2025-08-23T12:00:00',
        'cpu': 12.5,
        'ram': 43.2,
        'top_processes': [
            {'pid': 123, 'name': 'test_process', 'cpu_percent': 10.0}
        ]
    }

    storage.insert_metrics(mock_data)
    rows = storage.get_last_metrics(1)
    assert len(rows) == 1
    ts, cpu, ram, processes = rows[0]

    assert ts == mock_data['timestamp']
    assert abs(cpu - mock_data['cpu']) < 0.01
    assert abs(ram - mock_data['ram']) < 0.01

    loaded = json.loads(processes)
    assert loaded[0]['pid'] == 123
    assert loaded[0]['name'] == 'test_process'
    assert loaded[0]['cpu_percent'] == 10.0

def test_insert_fails_on_null_timestamp():
    """
    L'application doit tomber en erreur lors d'une valeur à NULL
    """
    bad_data = {
        'timestamp': None,
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)

def test_insert_with_invalid_cpu_type():
    """
    L'application doit tomber en erreur lors d'un type incorrect sur 'timestamp'
    """
    bad_data = {
        'timestamp': "not a datetime",
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)

def test_insert_with_invalid_cpu_type():
    """
    L'application doit tomber en erreur lors d'un type incorrect sur 'cpu'
    """
    bad_data = {
        'timestamp': '2025-08-23T14:00:00',
        'cpu': "not a float",
        'ram': 20.0,
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)

def test_insert_with_invalid_cpu_type():
    """
    L'application doit tomber en erreur lors d'un type incorrect sur 'ram'
    """
    bad_data = {
        'timestamp': '2025-08-23T14:00:00',
        'cpu': 10.0,
        'ram': "not a float",
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)

def test_insert_with_invalid_cpu_type():
    """
    L'application doit tomber en erreur lors d'un type incorrect sur 'top_processes'
    """
    bad_data = {
        'timestamp': '2025-08-23T14:00:00',
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': "not a list"
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)

def test_insert_with_non_serializable_processes():
    """
    L'application doit tomber en errur lors d'une valeur non sérialisable en JSON sur 'top_processes'
    """
    bad_data = {
        'timestamp': '2025-08-23T14:00:00',
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': set([1, 2, 3])
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data)