from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import ServiceResult, SystemMetrics

console = Console()


class ConsoleReporter:
    """Formats and prints check results using the Rich library."""

    @staticmethod
    def show_service_results(results: List[ServiceResult]):
        """Displays service health checks in a formatted table."""
        table = Table(title="🌐 SitePulse - Service Health Status", show_header=True, header_style="bold cyan")
        table.add_column("Status", justify="center", width=10)
        table.add_column("Service Name", style="bold white")
        table.add_column("URL", style="dim")
        table.add_column("HTTP Code", justify="center")
        table.add_column("Latency", justify="right")
        table.add_column("Details", style="italic")

        for res in results:
            status_badge = "[bold green]ONLINE[/bold green]" if res.is_healthy else "[bold red]OFFLINE[/bold red]"
            code_str = str(res.status_code) if res.status_code is not None else "-"
            latency_color = "green" if res.latency_ms < 200 else ("yellow" if res.latency_ms < 600 else "red")
            latency_str = f"[{latency_color}]{res.latency_ms} ms[/{latency_color}]"
            details = res.error_message if res.error_message else "[green]OK[/green]"

            table.add_row(
                status_badge,
                res.name,
                res.url,
                code_str,
                latency_str,
                details
            )

        console.print(table)

    @staticmethod
    def show_system_metrics(metrics: SystemMetrics):
        """Displays host system resource usage."""
        cpu_color = "green" if metrics.cpu_percent < 70 else ("yellow" if metrics.cpu_percent < 85 else "red")
        ram_color = "green" if metrics.ram_percent < 75 else "red"
        disk_color = "green" if metrics.disk_percent < 80 else "red"

        summary = (
            f"[bold]Timestamp:[/bold] {metrics.timestamp}\n\n"
            f"[bold cyan]CPU Utilization:[/bold cyan] [{cpu_color}]{metrics.cpu_percent}%[/{cpu_color}]\n"
            f"[bold cyan]RAM Memory:[/bold cyan] [{ram_color}]{metrics.ram_used_gb} GB / {metrics.ram_total_gb} GB ({metrics.ram_percent}%)[/{ram_color}]\n"
            f"[bold cyan]Disk Storage:[/bold cyan] [{disk_color}]{metrics.disk_free_gb} GB free / {metrics.disk_total_gb} GB total ({metrics.disk_percent}% used)[/{disk_color}]"
        )
        console.print(Panel(summary, title="💻 Local Host System Resources", border_style="cyan"))

    @staticmethod
    def show_history(history: List[ServiceResult]):
        """Displays historical checks from SQLite."""
        if not history:
            console.print("[yellow]No historical logs found in database.[/yellow]")
            return

        table = Table(title="📜 SitePulse - Recent Incident & Check Logs", show_header=True, header_style="bold magenta")
        table.add_column("Timestamp", style="dim")
        table.add_column("Status", justify="center")
        table.add_column("Service Name", style="bold")
        table.add_column("Latency", justify="right")
        table.add_column("Details")

        for item in history:
            badge = "[green]OK[/green]" if item.is_healthy else "[red]FAIL[/red]"
            table.add_row(
                item.timestamp,
                badge,
                item.name,
                f"{item.latency_ms} ms",
                item.error_message or "HTTP " + str(item.status_code)
            )

        console.print(table)

    @staticmethod
    def show_stats(stats: Dict[str, Any]):
        """Displays high level uptime statistics."""
        summary = (
            f"[bold]Total Checks Logged:[/bold] {stats['total_checks']}\n"
            f"[bold green]Successful Checks:[/bold green] {stats['healthy_checks']}\n"
            f"[bold red]Failed Checks:[/bold red] {stats['failed_checks']}\n"
            f"[bold cyan]Uptime Rate:[/bold cyan] {stats['uptime_percentage']}%\n"
            f"[bold yellow]Average Latency:[/bold yellow] {stats['avg_latency_ms']} ms"
        )
        console.print(Panel(summary, title="📊 Health & Uptime Statistics", border_style="green"))
