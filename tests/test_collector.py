from src.collector import (
    get_cpu_usage, get_ram_usage,
    get_top_processes, collect_metrics
)

def test_get_cpu_usage():
    """
    L'application doit pouvoir récupérer le taux d'utilisation courant du CPU
    """
    cpu = get_cpu_usage()
    assert isinstance(cpu, float)
    assert 0 <= cpu <= 100

def test_get_ram_usage():
    """
    L'application doit pouvoir récupérer le taux d'utilisation courant de la RAM
    """
    ram = get_ram_usage()
    assert isinstance(ram, float)
    assert 0 <= ram <= 100

def test_get_top_processes():
    """
    L'application doit pouvoir récupérer une liste de processus les plus consommateur du CPU
    """
    processes = get_top_processes()
    assert isinstance(processes, list)
    assert all('pid' in p and 'name' in p and 'cpu_percent' in p for p in processes)

def test_collect_metrics_structure():
    """
    L'application doit pouvoir collecter les données suivantes dans un dictionnaire : timestamp, cpu, ram, top_processes
    """
    data = collect_metrics()
    assert 'timestamp' in data
    assert 'cpu' in data
    assert 'ram' in data
    assert 'top_processes' in data
