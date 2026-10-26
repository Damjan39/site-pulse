import time
import requests
import psutil
from typing import Dict, Any
from .models import ServiceResult, SystemMetrics


class HealthChecker:
    """Performs network availability checks and system metric lookups."""

    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds

    def check_service(self, name: str, url: str) -> ServiceResult:
        """Pings an HTTP/HTTPS endpoint and measures latency."""
        start_time = time.perf_counter()
        try:
            response = requests.get(url, timeout=self.timeout)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            is_healthy = 200 <= response.status_code < 400

            return ServiceResult(
                name=name,
                url=url,
                status_code=response.status_code,
                latency_ms=elapsed_ms,
                is_healthy=is_healthy,
                error_message=None if is_healthy else f"HTTP {response.status_code}"
            )
        except requests.exceptions.Timeout:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return ServiceResult(
                name=name,
                url=url,
                status_code=None,
                latency_ms=elapsed_ms,
                is_healthy=False,
                error_message="Request Timeout"
            )
        except requests.exceptions.RequestException as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            # Short clean message
            err = type(e).__name__
            return ServiceResult(
                name=name,
                url=url,
                status_code=None,
                latency_ms=elapsed_ms,
                is_healthy=False,
                error_message=err
            )

    @staticmethod
    def get_system_metrics() -> SystemMetrics:
        """Retrieves host hardware utilization metrics."""
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return SystemMetrics(
            cpu_percent=cpu,
            ram_used_gb=round(mem.used / (1024 ** 3), 2),
            ram_total_gb=round(mem.total / (1024 ** 3), 2),
            ram_percent=mem.percent,
            disk_free_gb=round(disk.free / (1024 ** 3), 2),
            disk_total_gb=round(disk.total / (1024 ** 3), 2),
            disk_percent=disk.percent
        )
