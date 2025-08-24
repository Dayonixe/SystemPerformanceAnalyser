import pytest
from datetime import datetime
import json

from src import collector

def test_collect_metrics_timestamp_is_iso():
    """
    Le timestamp doit être une chaîne ISO 8601 valide
    """
    data = collector.collect_metrics()
    ts = data['timestamp']
    assert isinstance(ts, str)
    try:
        parsed = datetime.fromisoformat(ts)
    except ValueError:
        assert False, "timestamp is not a valid ISO format"

def test_get_cpu_usage():
    """
    L'application doit pouvoir récupérer le taux d'utilisation courant du CPU
    """
    cpu = collector.get_cpu_usage()
    assert isinstance(cpu, float)
    assert 0 <= cpu <= 100

def test_get_max_cpu_percent():
    """
    L'application doit avoir une valeur maximale d'utilisation CPU doit être un float supérieur ou égal à 100% (valable pour les machines avec au moins 1 cœur)
    """
    from src.collector import get_max_cpu_percent
    max_cpu = get_max_cpu_percent()
    assert isinstance(max_cpu, float)
    assert max_cpu >= 100.0

def test_get_ram_usage():
    """
    L'application doit pouvoir récupérer le taux d'utilisation courant de la RAM
    """
    ram = collector.get_ram_usage()
    assert isinstance(ram, float)
    assert 0 <= ram <= 100

def test_get_top_processes():
    """
    L'application doit pouvoir récupérer une liste de processus les plus consommateur du CPU
    """
    processes = collector.get_top_processes()
    assert isinstance(processes, list)
    assert all('pid' in p and 'name' in p and 'cpu_percent' in p for p in processes)

def test_get_top_processes_with_zero():
    """
    get_top_processes() doit retourner une liste vide si top_n=0
    """
    processes = collector.get_top_processes(top_n=0)
    assert processes == []

@pytest.mark.parametrize("n", [1, 3, 5, 10])
def test_get_top_processes_various_n(n):
    """
    get_top_processes() doit récupérer une liste de processus les plus consommateur du CPU pour diverse valeur de top_n
    """
    processes = collector.get_top_processes(top_n=n)
    assert len(processes) <= n

def test_get_top_processes_values():
    """
    L'application doit, pour chaque processus retourné, avoir des valeurs cohérentes
    """
    processes = collector.get_top_processes()
    max_cpu = collector.get_max_cpu_percent()

    # En CI ou VM, psutil peut surestimer le cpu_percent
    # On tolère jusqu’à +20% du max théorique
    margin = max_cpu * 0.2  # tolérance de 20%

    for proc in processes:
        assert isinstance(proc['pid'], int)
        assert isinstance(proc['name'], str)
        assert isinstance(proc['cpu_percent'], float)
        assert 0.0 <= proc['cpu_percent'] <= max_cpu + margin

def test_collect_metrics_structure():
    """
    L'application doit pouvoir collecter les données suivantes dans un dictionnaire : timestamp, cpu, ram, top_processes
    """
    data = collector.collect_metrics()
    assert 'timestamp' in data
    assert 'cpu' in data
    assert 'ram' in data
    assert 'top_processes' in data

def test_collect_metrics_data_content():
    """
    L'application ne doit pas avoir de perte sur la cohérence des données collectées
    """
    data = collector.collect_metrics()

    # timestamp
    ts = data['timestamp']
    assert isinstance(ts, str)
    datetime.fromisoformat(ts)

    # CPU / RAM
    assert isinstance(data['cpu'], float)
    assert 0 <= data['cpu'] <= 100
    assert isinstance(data['ram'], float)
    assert 0 <= data['ram'] <= 100

    # Processus
    processes = data['top_processes']
    assert isinstance(processes, list)
    for proc in processes:
        assert isinstance(proc['pid'], int)
        assert isinstance(proc['name'], str)
        assert isinstance(proc['cpu_percent'], float)

    # Vérifie que JSON serialization fonctionne (utile pour stockage)
    json_string = json.dumps(processes)
    assert isinstance(json_string, str)