import argparse
import time
from datetime import datetime, timedelta

from src import collector, storage, report

def collect_command(args):
    """
    Commande de collecte de données sur une période donnée
    :param args: interval : Temps en seconde entre 2 récupération de données ; duration : Durée de récupération des données
    """
    print(f"Collecting metrics every {args.interval}s for {args.duration}s...")
    # storage.delete_database()
    storage.init_database()
    start_time = time.time()
    while time.time() - start_time < args.duration:
        data = collector.collect_metrics()
        storage.insert_metrics(data)
        print(f"[{data['timestamp']}] CPU: {data['cpu']}% | RAM: {data['ram']}%")
        time.sleep(args.interval)

def parse_time_filter(args):
    """
    Filtre des valeurs de manière temporelle
    :param args: since : Date de début des données à afficher ; last : Pour afficher la dernière heure ou jour d'enregistrement
    :return: Date de début des données à afficher
    """
    if args.since:
        return datetime.fromisoformat(args.since)
    elif args.last == "hour":
        return datetime.now() - timedelta(hours=1)
    elif args.last == "day":
        return datetime.now() - timedelta(days=1)
    return None

def main():
    parser = argparse.ArgumentParser(description="System Monitor CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Commande : collect
    collect_parser = subparsers.add_parser("collect", help="Collect system metrics")
    collect_parser.add_argument("--interval", type=int, default=5, help="Interval between collections (in seconds)")
    collect_parser.add_argument("--duration", type=int, default=60, help="Total duration of the collection (in seconds)")
    collect_parser.set_defaults(func=collect_command)

    # Commande : report
    report_parser = subparsers.add_parser("report", help="Generate performance report")
    report_parser.add_argument("--limit", type=int, default=100, help="Number of data points to include")
    report_parser.add_argument("--since", type=str, help="Start datetime (ISO format: YYYY-MM-DDTHH:MM)")
    report_parser.add_argument("--last", choices=["hour", "day"], help="Use a pre-defined time filter")
    report_parser.add_argument("--save", action="store_true", help="Save report as PNG instead of showing it")
    report_parser.set_defaults(func=lambda args: report.generate_plot(limit=args.limit, since=parse_time_filter(args), save=args.save))

    # Parse & exécute
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()