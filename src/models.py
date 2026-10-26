from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ServiceResult:
    """Represents the outcome of a single endpoint health check."""
    name: str
    url: str
    status_code: Optional[int]
    latency_ms: float
    is_healthy: bool
    error_message: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class SystemMetrics:
    """Represents host system resource utilization."""
    cpu_percent: float
    ram_used_gb: float
    ram_total_gb: float
    ram_percent: float
    disk_free_gb: float
    disk_total_gb: float
    disk_percent: float
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
