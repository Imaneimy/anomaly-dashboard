# anomaly-dashboard

When you're running multiple test campaigns across different pipelines and sprints, tracking anomalies in a spreadsheet stops working pretty fast. This is a lightweight alternative — a local SQLite-backed tracker with a generated HTML dashboard, inspired by how JIRA and XRAY handle test defects.

Each anomaly has a title, description, severity (CRITICAL / HIGH / MEDIUM / LOW), status (OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED / WONT_FIX), component, sprint, tags, and a comment thread. The dashboard shows KPI counts and a status distribution bar. Everything runs locally, no server needed.

## Structure

```
src/
  anomaly_tracker.py    # CRUD operations on SQLite — create, update, filter, stats
  dashboard.py          # generates the HTML dashboard from tracker data
  run_dashboard.py      # seeds sample data and opens the dashboard

tests/
  test_anomaly_tracker.py   # 10 unit tests

data/
  anomalies.db          # SQLite file (created on first run)
  dashboard.html        # the generated report
```

## Running it

```bash
pip install -r requirements.txt
cd src
python run_dashboard.py
```

This seeds the database with 10 sample anomalies pulled from the other three projects in this portfolio (ETL pipeline issues, Datalake drift, SQL validation failures) and opens the dashboard in your browser.

```bash
pytest tests/ -v
```

## Using the tracker in your own tests

```python
from anomaly_tracker import AnomalyTracker, Anomaly

tracker = AnomalyTracker("anomalies.db")

# Log an anomaly from a test
tracker.create(Anomaly(
    title="NULL customer_id in fact_sales",
    description="10 rows passed Silver layer with customer_id=NULL",
    severity="HIGH",
    status="OPEN",
    project="DataMart-Q1",
    component="ETL",
    detected_by="TC-REG-002",
    sprint="Sprint-01"
))

# Filter
open_high = tracker.list_all(status="OPEN", severity="HIGH")

# Stats for dashboard
print(tracker.get_stats())
```

## Stack

Python, Python, SQLite, HTML/CSS

