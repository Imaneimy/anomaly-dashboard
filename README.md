# Anomaly Dashboard — Big Data Test Tracker

Test anomaly tracking tool for Big Data projects, inspired by JIRA/XRAY workflows. Manages tickets with severity, status, sprint, and comments. Generates a local HTML dashboard showing KPIs and anomaly distribution across components.

---

## Project structure

```
04_anomaly_dashboard/
├── src/
│   ├── anomaly_tracker.py    # SQLite CRUD — anomaly tickets
│   ├── dashboard.py          # HTML dashboard generator
│   └── run_dashboard.py      # Entry point — seed data + generate report
├── tests/
│   └── test_anomaly_tracker.py   # TC-DASH-001 to TC-DASH-010
└── data/
    ├── anomalies.db          # SQLite database (generated)
    └── dashboard.html        # HTML dashboard (generated)
```

---

## Setup

```bash
pip install -r requirements.txt

cd src
python run_dashboard.py

# Open dashboard (macOS)
open ../data/dashboard.html

# Run tests
pytest tests/ -v
```

---

## Features

| Feature | Description |
|---------|-------------|
| Create anomaly | Title, description, severity, status, sprint, tags |
| Update status | OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED |
| Comments | Discussion thread per anomaly |
| Filters | By status, severity, component |
| KPIs | Total, Open, In Progress, Resolved, Open Critical |
| HTML report | Interactive dashboard generated locally |

---

## Severity and status definitions

| Severity | Examples |
|----------|---------|
| CRITICAL | Data corruption, reconciliation failure |
| HIGH | Orphan FK, NULL on mandatory column |
| MEDIUM | Missing filter, wrong format |
| LOW | Unexpected column, minor statistical drift |

| Status | Description |
|--------|-------------|
| OPEN | Detected, not yet assigned |
| IN_PROGRESS | Under investigation or fix |
| RESOLVED | Fix deployed, pending validation |
| CLOSED | Validated and closed |
| WONT_FIX | Decision not to fix |

---

## Sample anomalies

The dashboard is pre-loaded with 10 realistic anomalies sourced from the other three portfolio projects, covering ETL, Datalake, and SQL validation contexts.

---

## Stack

Python / SQLite / HTML + CSS

---

## Author

Imane Moussafir — Data & BI Engineer
