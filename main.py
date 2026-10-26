import argparse
import json
import os
import sys
import time
from typing import Dict, Any

from src.checker import HealthChecker
from src.database import DatabaseManager
from src.reporter import ConsoleReporter, console


CONFIG_FILE = "config.json"


def load_config() -> Dict[str, Any]:
    """Loads configuration settings and targets from JSON."""
    if not os.path.exists(CONFIG_FILE):
        console.print(f"[bold red]Error:[/bold red] Configuration file '{CONFIG_FILE}' not found.")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def run_service_checks(config: Dict[str, Any], db: DatabaseManager):
    """Executes checks for all endpoints in config."""
    checker = HealthChecker(timeout_seconds=config.get("timeout_seconds", 5))
    endpoints = config.get("endpoints", [])
    
    with console.status("[bold cyan]Running health checks...", spinner="dots"):
        results = []
        for ep in endpoints:
            res = checker.check_service(ep["name"], ep["url"])
            db.save_result(res)
            results.append(res)
    
    ConsoleReporter.show_service_results(results)


def run_system_check():
    """Reads and displays host machine metrics."""
    metrics = HealthChecker.get_system_metrics()
    ConsoleReporter.show_system_metrics(metrics)


def main():
    parser = argparse.ArgumentParser(
        description="SitePulse - Lightweight IT Service & System Health Monitor"
    )
    parser.add_argument("--check", action="store_true", help="Run a full health check on all endpoints")
    parser.add_argument("--system", action="store_true", help="Display local system hardware metrics")
    parser.add_argument("--history", action="store_true", help="Display recent health check logs from SQLite")
    parser.add_argument("--stats", action="store_true", help="Display aggregate uptime and latency statistics")
    parser.add_argument("--watch", action="store_true", help="Run monitoring continuously in a loop")
    parser.add_argument("--interval", type=int, default=15, help="Interval in seconds for watch mode (default: 15)")

    args = parser.parse_args()
    config = load_config()
    db = DatabaseManager()

    # If no flags are passed, run check + system overview by default
    if not (args.check or args.system or args.history or args.stats or args.watch):
        console.rule("[bold cyan]SitePulse - Infrastructure Health Monitor[/bold cyan]")
        run_system_check()
        run_service_checks(config, db)
        ConsoleReporter.show_stats(db.get_stats())
        console.print("\n[dim]Tip: Use `python main.py --help` to see all available CLI commands.[/dim]\n")
        return

    if args.system:
        run_system_check()

    if args.check:
        run_service_checks(config, db)

    if args.history:
        ConsoleReporter.show_history(db.get_recent_history())

    if args.stats:
        ConsoleReporter.show_stats(db.get_stats())

    if args.watch:
        console.print(f"[bold green]Starting live monitor mode (polling every {args.interval}s)... Press Ctrl+C to stop.[/bold green]\n")
        try:
            while True:
                console.rule(f"[cyan]Inspection Run: {time.strftime('%H:%M:%S')}[/cyan]")
                run_service_checks(config, db)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Monitoring stopped by user.[/bold yellow]")


if __name__ == "__main__":
    main()
