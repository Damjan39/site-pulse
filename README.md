# SitePulse - IT Service & System Health Monitor

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A automated infrastructure monitoring tool written in Python. `SitePulse` continuously tracks the availability and latency of web services, monitors host system resources (CPU, Memory, Disk), and logs incidents into a persistent SQLite database with rich terminal visualization.

---

## Features

- **Service Health Checks:** Checks HTTP status codes, latency (ms), and server availability.
- **Local System Metrics:** Inspects CPU usage, RAM utilization, and disk space.
- **Persistent Incident Log:** Stores all check results and outages in an SQLite database.
- **Rich Terminal UI:** Formatted colored tables, status badges, and summary statistics powered by `rich`.
- **JSON Configurable:** Easily add or remove target URLs, ports, and threshold alerts in `config.json`.
- **Exportable Reports:** Generates incident summaries and system health overviews.

---

## Tech Stack & Concepts

- **Language:** Python 3.10+
- **Architecture:** Clean Object-Oriented Design (OOP) with Dataclasses & Type Hinting
- **Libraries:**
  - `requests`: HTTP network checks & latency profiling
  - `psutil`: Hardware and OS process monitoring
  - `rich`: Modern terminal tables, formatting, and live status displays
  - `sqlite3`: Native relational database storage

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<YOUR-USERNAME>/site-pulse.git
   cd site-pulse
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Run a quick one-time health check
```bash
python main.py --check
```

### 2. View local system health (CPU, RAM, Disk)
```bash
python main.py --system
```

### 3. View past check history from the SQLite database
```bash
python main.py --history
```

### 4. Continuous live monitoring loop (every 30 seconds)
```bash
python main.py --watch --interval 30
```

---

## Configuration

You can customize targets and timeouts in `config.json`:

```json
{
  "timeout_seconds": 5,
  "endpoints": [
    {
      "name": "Google DNS / Web",
      "url": "https://www.google.com"
    },
    {
      "name": "GitHub Platform",
      "url": "https://github.com"
    },
    {
      "name": "Local API",
      "url": "http://localhost:8000"
    }
  ]
}
```

---

## Author
- **HTL IT Student**
- GitHub: [@Damjan39](https://github.com/)
