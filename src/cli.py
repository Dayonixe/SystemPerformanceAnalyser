import argparse
import time
import json
from src import collector, storage

def collect_command(args):
    print(f"Collecting metrics every {args.interval}s for {args.duration}s...")
    storage.delete_database()
    storage.init_database()
    start_time = time.time()
    while time.time() - start_time < args.duration:
        data = collector.collect_metrics()
        storage.insert_metrics(data)
        print(f"[{data['timestamp']}] CPU: {data['cpu']}% | RAM: {data['ram']}%")
        time.sleep(args.interval)

def show_command(args):
    rows = storage.get_last_metrics(limit=args.limit)
    for row in rows:
        timestamp, cpu, ram, top = row
        print(f"[{timestamp}] CPU: {cpu}% | RAM: {ram}%")
        processes = json.loads(top)
        for p in processes:
            name = p.get('name', 'unknown')
            pid = p.get('pid', '-')
            cpu_p = p.get('cpu_percent', '?')
            print(f"  ↳ PID {pid:<5} | {name:<20} | CPU: {cpu_p}%")

def main():
    parser = argparse.ArgumentParser(description="System Monitor CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Commande : collect
    collect_parser = subparsers.add_parser("collect", help="Collect system metrics")
    collect_parser.add_argument("--interval", type=int, default=5, help="Interval between collections (in seconds)")
    collect_parser.add_argument("--duration", type=int, default=60, help="Total duration of the collection (in seconds)")
    collect_parser.set_defaults(func=collect_command)

    # Commande : show
    show_parser = subparsers.add_parser("show", help="Show last collected metrics")
    show_parser.add_argument("--limit", type=int, default=5, help="Number of rows to display")
    show_parser.set_defaults(func=show_command)

    # Parse & exécute
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
