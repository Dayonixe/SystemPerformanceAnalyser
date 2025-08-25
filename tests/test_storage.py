import pytest
import sqlite3
import os
import json
from datetime import datetime, timedelta

from src import collector, storage
from config.config import DB_TEST_PATH

@pytest.fixture(autouse=True)
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
    storage.insert_metrics(data, DB_TEST_PATH)

    ts, cpu, ram, processes = storage.get_last_metrics(1, DB_TEST_PATH)

    assert isinstance(ts[0], datetime)

    assert isinstance(cpu[0], float)
    assert isinstance(ram[0], float)

    proc_list = json.loads(processes[0])
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

    storage.insert_metrics(mock_data, DB_TEST_PATH)
    ts, cpu, ram, processes = storage.get_last_metrics(1, DB_TEST_PATH)

    assert ts[0] == datetime.fromisoformat(mock_data['timestamp'])
    assert abs(cpu[0] - mock_data['cpu']) < 0.01
    assert abs(ram[0] - mock_data['ram']) < 0.01

    loaded = json.loads(processes[0])
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
        storage.insert_metrics(bad_data, DB_TEST_PATH)

def test_insert_with_invalid_timestamp_type_1():
    """
    L'application doit tomber en erreur lors d'un bon type mais au mauvais format sur 'timestamp'
    """
    bad_data = {
        'timestamp': "not a datetime",
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data, DB_TEST_PATH)

def test_insert_with_invalid_timestamp_type_2():
    """
    L'application doit tomber en erreur lors d'un type incorrect sur 'timestamp'
    """
    bad_data = {
        'timestamp': 12345,
        'cpu': 10.0,
        'ram': 20.0,
        'top_processes': []
    }

    with pytest.raises(TypeError):
        storage.insert_metrics(bad_data, DB_TEST_PATH)

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
        storage.insert_metrics(bad_data, DB_TEST_PATH)

def test_insert_with_invalid_ram_type():
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
        storage.insert_metrics(bad_data, DB_TEST_PATH)

def test_insert_with_invalid_top_processes_type():
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
        storage.insert_metrics(bad_data, DB_TEST_PATH)

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
        storage.insert_metrics(bad_data, DB_TEST_PATH)

def test_get_last_time_metrics_returns_correct_data():
    """
    L'application doit pouvoir renvoyer uniquement les métriques postérieures à une date donnée
    """
    # Insertion de 3 lignes espacées dans le temps
    base_time = datetime(2025, 8, 23, 15, 0, 0)
    for i in range(3):
        mock_data = {
            'timestamp': (base_time + timedelta(seconds=i)).isoformat(),
            'cpu': 10.0 + i,
            'ram': 30.0 + i,
            'top_processes': []
        }
        storage.insert_metrics(mock_data, DB_TEST_PATH)

    # On interroge à partir de la 2e
    since = base_time + timedelta(seconds=1)
    ts, cpu, ram, processes = storage.get_last_time_metrics(since, DB_TEST_PATH)

    assert len(ts) == 2
    assert ts[0] == base_time + timedelta(seconds=1)
    assert cpu == [11.0, 12.0]
    assert ram == [31.0, 32.0]

def test_get_last_time_metrics_with_future_date_returns_empty():
    """
    L'application ne doit rien retourner si la date 'since' est dans le futur
    """
    future = datetime.now() + timedelta(days=365)
    ts, cpu, ram, processes = storage.get_last_time_metrics(future, DB_TEST_PATH)

    assert ts == []
    assert cpu == []
    assert ram == []
    assert processes == []

def test_get_last_time_metrics_includes_exact_match():
    """
    L'application doit inclure les données dont le timestamp est exactement égal à la date 'since'
    """
    # Timestamp exact à tester
    exact_time = datetime(2025, 8, 23, 16, 0, 0)
    storage.insert_metrics({
        'timestamp': exact_time.isoformat(),
        'cpu': 42.0,
        'ram': 84.0,
        'top_processes': []
    }, DB_TEST_PATH)

    ts, cpu, ram, _ = storage.get_last_time_metrics(exact_time, DB_TEST_PATH)
    assert exact_time in ts
    assert 42.0 in cpu
    assert 84.0 in ram

def test_get_last_time_metrics_with_none_raises():
    """
    L'application doit lever une exception si 'since' est None
    """
    with pytest.raises(ValueError):
        storage.get_last_time_metrics(None, DB_TEST_PATH)

def test_get_last_time_metrics_returns_sorted_data():
    """
    Les données retournées doivent être triées chronologiquement croissante (ASC)
    """
    times = [
        datetime(2025, 8, 23, 18, 0, 10),
        datetime(2025, 8, 23, 18, 0, 5),
        datetime(2025, 8, 23, 18, 0, 20)
    ]

    for t in times:
        storage.insert_metrics({
            'timestamp': t.isoformat(),
            'cpu': 10.0,
            'ram': 10.0,
            'top_processes': []
        }, DB_TEST_PATH)

    ts, _, _, _ = storage.get_last_time_metrics(datetime(2025, 8, 23, 18, 0, 0), DB_TEST_PATH)

    assert ts == sorted(ts)