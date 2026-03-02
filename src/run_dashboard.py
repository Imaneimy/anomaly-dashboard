"""
Entry point — generates the anomaly dashboard HTML file.
"""

import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from anomaly_tracker import AnomalyTracker
from dashboard import generate_dashboard, seed_sample_data

BASE = Path(__file__).resolve().parents[1]
DB_PATH = str(BASE / "data/anomalies.db")
OUTPUT_HTML = str(BASE / "data/dashboard.html")


def main():
    os.makedirs(str(BASE / "data"), exist_ok=True)
    tracker = AnomalyTracker(db_path=DB_PATH)
    seed_sample_data(tracker)

    stats = tracker.get_stats()
    print(f"Loaded {stats['total']} anomalies — Open critical: {stats['open_critical']}")

    path = generate_dashboard(tracker, OUTPUT_HTML, sprint="Sprint-01 → Sprint-03")
    print(f"Dashboard generated: {path}")

    try:
        import subprocess
        subprocess.run(["open", path])
    except Exception:
        pass


if __name__ == "__main__":
    main()
