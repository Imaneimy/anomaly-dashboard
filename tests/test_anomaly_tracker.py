"""
Unit Tests — AnomalyTracker
XRAY IDs: TC-DASH-001 → TC-DASH-010
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import pytest
from anomaly_tracker import AnomalyTracker, Anomaly


@pytest.fixture
def tracker():
    return AnomalyTracker(db_path=":memory:")


def make_anomaly(**kwargs) -> Anomaly:
    defaults = dict(
        title="Test anomaly",
        description="Desc",
        severity="HIGH",
        status="OPEN",
        project="TestProject",
        component="ETL",
        detected_by="TC-001",
    )
    defaults.update(kwargs)
    return Anomaly(**defaults)


# ---------------------------------------------------------------------------
# TC-DASH-001 | Create anomaly and retrieve it
# ---------------------------------------------------------------------------
def test_create_and_get(tracker):
    a = make_anomaly(title="NULL customer found")
    aid = tracker.create(a)
    retrieved = tracker.get(aid)
    assert retrieved is not None
    assert retrieved["title"] == "NULL customer found"


# ---------------------------------------------------------------------------
# TC-DASH-002 | Update status to RESOLVED sets resolved_at
# ---------------------------------------------------------------------------
def test_update_status_resolved(tracker):
    a = make_anomaly()
    aid = tracker.create(a)
    tracker.update_status(aid, "RESOLVED")
    updated = tracker.get(aid)
    assert updated["status"] == "RESOLVED"
    assert updated["resolved_at"] is not None


# ---------------------------------------------------------------------------
# TC-DASH-003 | Update status to IN_PROGRESS does not set resolved_at
# ---------------------------------------------------------------------------
def test_update_status_in_progress(tracker):
    a = make_anomaly()
    aid = tracker.create(a)
    tracker.update_status(aid, "IN_PROGRESS")
    updated = tracker.get(aid)
    assert updated["status"] == "IN_PROGRESS"
    assert updated["resolved_at"] is None


# ---------------------------------------------------------------------------
# TC-DASH-004 | list_all returns all anomalies
# ---------------------------------------------------------------------------
def test_list_all(tracker):
    for i in range(3):
        tracker.create(make_anomaly(title=f"Anomaly {i}"))
    all_a = tracker.list_all()
    assert len(all_a) == 3


# ---------------------------------------------------------------------------
# TC-DASH-005 | Filter by status
# ---------------------------------------------------------------------------
def test_list_filter_status(tracker):
    tracker.create(make_anomaly(status="OPEN"))
    tracker.create(make_anomaly(status="RESOLVED"))
    open_list = tracker.list_all(status="OPEN")
    assert len(open_list) == 1
    assert open_list[0]["status"] == "OPEN"


# ---------------------------------------------------------------------------
# TC-DASH-006 | Filter by severity
# ---------------------------------------------------------------------------
def test_list_filter_severity(tracker):
    tracker.create(make_anomaly(severity="CRITICAL"))
    tracker.create(make_anomaly(severity="LOW"))
    critical = tracker.list_all(severity="CRITICAL")
    assert len(critical) == 1


# ---------------------------------------------------------------------------
# TC-DASH-007 | Filter by component
# ---------------------------------------------------------------------------
def test_list_filter_component(tracker):
    tracker.create(make_anomaly(component="ETL"))
    tracker.create(make_anomaly(component="SQL"))
    etl = tracker.list_all(component="ETL")
    assert len(etl) == 1


# ---------------------------------------------------------------------------
# TC-DASH-008 | get_stats returns correct totals
# ---------------------------------------------------------------------------
def test_get_stats(tracker):
    tracker.create(make_anomaly(severity="CRITICAL", status="OPEN"))
    tracker.create(make_anomaly(severity="HIGH", status="RESOLVED"))
    tracker.create(make_anomaly(severity="CRITICAL", status="OPEN"))
    stats = tracker.get_stats()
    assert stats["total"] == 3
    assert stats["open_critical"] == 2
    assert stats["by_status"]["OPEN"] == 2
    assert stats["by_status"]["RESOLVED"] == 1


# ---------------------------------------------------------------------------
# TC-DASH-009 | Add comment and verify stored
# ---------------------------------------------------------------------------
def test_add_comment(tracker):
    a = make_anomaly()
    aid = tracker.create(a)
    tracker.add_comment(aid, "Imane M.", "Root cause identified.")
    rows = tracker.conn.execute(
        "SELECT * FROM comments WHERE anomaly_id=?", (aid,)
    ).fetchall()
    assert len(rows) == 1
    assert rows[0]["body"] == "Root cause identified."


# ---------------------------------------------------------------------------
# TC-DASH-010 | get returns None for unknown ID
# ---------------------------------------------------------------------------
def test_get_unknown(tracker):
    result = tracker.get("UNKNOWN_ID")
    assert result is None
