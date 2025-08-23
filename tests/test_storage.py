import json
from src import collector, storage

def test_storage_insert_and_read():
    """
    L'application doit pouvoir initier la base de données au besoin, ajouter et lire des données dans la base de données
    """
    storage.init_database()
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
