import psutil
import datetime

def get_timestamp():
    """
    Récupération de la date courante
    :return: Date courante
    """
    return datetime.datetime.now().isoformat()

def get_cpu_usage():
    """
    Récupération du pourcentage de l'utilisation CPU courante
    :return: Utilisation CPU courante
    """
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    """
    Récupération du pourcentage de l'utilisation RAM courante
    :return: Utilisation RAM courante
    """
    return psutil.virtual_memory().percent

def get_top_processes(top_n=5):
    """
    Récupération des processus en cours qui consomme le plus de CPU
    :param top_n: nombre de processus à récupérer
    :return: Liste des processus en cours qui consomme le plus de CPU
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            processes.append(info)
        except psutil.NoSuchProcess:
            continue

    return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:top_n]

def collect_metrics():
    """
    Récupération des différentes métriques
    :return:
    """
    return {
        'timestamp': get_timestamp(),
        'cpu': get_cpu_usage(),
        'ram': get_ram_usage(),
        'top_processes': get_top_processes()
    }
