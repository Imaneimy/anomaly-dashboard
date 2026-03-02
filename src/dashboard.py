"""
Anomaly Dashboard — HTML generator
Produces a JIRA-like visual dashboard from the AnomalyTracker database.
"""

import os
from datetime import datetime
from typing import List, Dict
from anomaly_tracker import AnomalyTracker, Anomaly


SEVERITY_COLORS = {
    "CRITICAL": ("#fde8e8", "#c0392b"),
    "HIGH":     ("#fff3e0", "#e67e22"),
    "MEDIUM":   ("#fef9e7", "#d4ac0d"),
    "LOW":      ("#eaf4fb", "#2471a3"),
}

STATUS_COLORS = {
    "OPEN":        ("#fde8e8", "#c0392b"),
    "IN_PROGRESS": ("#fff3e0", "#e67e22"),
    "RESOLVED":    ("#eafaf1", "#1e8449"),
    "CLOSED":      ("#eaf0fb", "#2e4057"),
    "WONT_FIX":    ("#f4f4f4", "#7f8c8d"),
}


def _badge(text: str, bg: str, color: str) -> str:
    return (
        f'<span style="background:{bg};color:{color};padding:3px 10px;'
        f'border-radius:12px;font-size:0.78em;font-weight:bold">{text}</span>'
    )


def generate_dashboard(tracker: AnomalyTracker, output_path: str,
                        sprint: str = "Sprint-01") -> str:
    stats = tracker.get_stats()
    anomalies = tracker.list_all()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ── KPI cards ────────────────────────────────────────────────────────────
    kpi_html = ""
    kpi_data = [
        ("Total Anomalies", stats["total"], "#3498db"),
        ("🔴 Open",         stats["by_status"].get("OPEN", 0), "#e74c3c"),
        ("🔄 In Progress",  stats["by_status"].get("IN_PROGRESS", 0), "#e67e22"),
        ("✅ Resolved",     stats["by_status"].get("RESOLVED", 0), "#27ae60"),
        ("🚨 Open Critical",stats["open_critical"], "#8e44ad"),
    ]
    for label, value, color in kpi_data:
        kpi_html += f"""
        <div class="kpi-card">
          <div class="kpi-value" style="color:{color}">{value}</div>
          <div class="kpi-label">{label}</div>
        </div>"""

    # ── Status breakdown bar ─────────────────────────────────────────────────
    total = stats["total"] or 1
    bar_html = ""
    for status, count in stats["by_status"].items():
        pct = count / total * 100
        bg, _ = STATUS_COLORS.get(status, ("#ccc", "#333"))
        bar_html += (
            f'<div style="width:{pct:.1f}%;background:{bg};height:100%;'
            f'display:inline-block;vertical-align:top" title="{status}: {count}"></div>'
        )

    # ── Anomaly rows ─────────────────────────────────────────────────────────
    rows_html = ""
    for a in anomalies:
        sev_bg, sev_col = SEVERITY_COLORS.get(a["severity"], ("#eee", "#333"))
        sta_bg, sta_col = STATUS_COLORS.get(a["status"], ("#eee", "#333"))
        rows_html += f"""
        <tr>
          <td><code style="font-size:0.8em">ANO-{a['anomaly_id']}</code></td>
          <td><strong>{a['title']}</strong><br>
            <small style="color:#7f8c8d">{a['description'][:80]}…</small></td>
          <td>{_badge(a['severity'], sev_bg, sev_col)}</td>
          <td>{_badge(a['status'], sta_bg, sta_col)}</td>
          <td><span class="comp-badge">{a['component']}</span></td>
          <td style="font-size:0.8em;color:#666">{a['detected_by']}</td>
          <td style="font-size:0.8em">{a['sprint']}</td>
          <td style="font-size:0.8em;color:#666">{a['created_at'][:10]}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Anomaly Dashboard — {sprint}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; }}
    .header {{ background: #2c3e50; color: white; padding: 18px 30px; display: flex; justify-content: space-between; align-items: center; }}
    .header h1 {{ font-size: 1.4em; }}
    .header .sub {{ font-size: 0.85em; opacity: 0.7; }}
    .content {{ padding: 24px 30px; }}
    .kpi-row {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .kpi-card {{ background: white; border-radius: 10px; padding: 18px 24px; flex: 1; min-width: 140px;
                 box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
    .kpi-value {{ font-size: 2.4em; font-weight: 700; }}
    .kpi-label {{ font-size: 0.82em; color: #7f8c8d; margin-top: 4px; }}
    .section {{ background: white; border-radius: 10px; padding: 20px 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 24px; }}
    .section h2 {{ font-size: 1em; color: #2c3e50; margin-bottom: 14px; border-bottom: 2px solid #ecf0f1; padding-bottom: 8px; }}
    .progress-bar {{ height: 18px; background: #ecf0f1; border-radius: 9px; overflow: hidden; margin-bottom: 8px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.88em; }}
    th {{ background: #2c3e50; color: white; padding: 10px 12px; text-align: left; font-weight: 600; }}
    td {{ padding: 10px 12px; border-bottom: 1px solid #ecf0f1; vertical-align: middle; }}
    tr:hover {{ background: #f8f9fa; }}
    .comp-badge {{ background: #eaf4fb; color: #2471a3; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }}
    .legend {{ display: flex; gap: 14px; flex-wrap: wrap; font-size: 0.82em; color: #555; margin-top: 8px; }}
    .footer {{ text-align: center; color: #aaa; font-size: 0.8em; padding: 16px; }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>🔬 Big Data Anomaly Dashboard</h1>
      <div class="sub">Suivi des anomalies de test | {sprint}</div>
    </div>
    <div style="font-size:0.85em;opacity:0.8">
      Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
    </div>
  </div>

  <div class="content">
    <!-- KPIs -->
    <div class="kpi-row">{kpi_html}</div>

    <!-- Status bar -->
    <div class="section">
      <h2>📊 Status Distribution</h2>
      <div class="progress-bar">{bar_html}</div>
      <div class="legend">
        {''.join(f'<span>{_badge(s, *STATUS_COLORS.get(s, ("#eee","#333")))} {stats["by_status"].get(s, 0)}</span>'
                  for s in ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED", "WONT_FIX"])}
      </div>
    </div>

    <!-- Anomaly table -->
    <div class="section">
      <h2>🐛 Anomalies ({len(anomalies)})</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Titre</th><th>Sévérité</th><th>Statut</th>
            <th>Composant</th><th>Détecté par</th><th>Sprint</th><th>Date</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>

  <div class="footer">Imane Moussafir — Big Data Anomaly Dashboard | {sprint}</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def seed_sample_data(tracker: AnomalyTracker) -> None:
    """Populate the tracker with realistic sample anomalies."""
    samples = [
        Anomaly("NULL customer_id in fact_sales",
                "10 rows with NULL customer_id found after Silver transformation. ETL filter not applied.",
                "HIGH", "OPEN", "DataMart-Q1", "ETL", "TC-REG-002", sprint="Sprint-01",
                tags="null,etl,silver"),
        Anomaly("Negative total_amount in S011",
                "Sale S011 has total_amount=-59.98. Business rule DQ-014 triggered.",
                "CRITICAL", "IN_PROGRESS", "DataMart-Q1", "SQL", "DQ-014", sprint="Sprint-01",
                tags="amount,negative,critical"),
        Anomaly("Orphan FK C999 in fact_sales",
                "customer_id=C999 not present in dim_customer. Referential integrity broken.",
                "HIGH", "OPEN", "DataMart-Q1", "SQL", "DQ-012", sprint="Sprint-01",
                tags="fk,orphan,dim_customer"),
        Anomaly("CANCELLED status not filtered in Bronze→Silver",
                "11 rows with status=CANCELLED passed to Silver layer. Filter regex missing.",
                "MEDIUM", "RESOLVED", "Datalake", "DATALAKE", "TC-REG-004", sprint="Sprint-01",
                tags="status,filter,bronze"),
        Anomaly("Duplicate event_id E001 in Bronze",
                "event_id E001 appears twice in Bronze layer. Dedup not applied at source.",
                "MEDIUM", "CLOSED", "Datalake", "DATALAKE", "TC-REG-005", sprint="Sprint-01",
                tags="dedup,duplicate,bronze"),
        Anomaly("Gold reconciliation drift 1.8%",
                "Sum mismatch between Silver COMPLETED and Gold total_amount: 1.8% drift detected.",
                "HIGH", "OPEN", "Datalake", "DATALAKE", "TC-GOLD-006", sprint="Sprint-02",
                tags="reconciliation,drift,gold"),
        Anomaly("event_date cast failure on 3 rows",
                "3 rows with event_date='N/A' cannot be parsed to TimestampType. Bronze data quality issue.",
                "MEDIUM", "IN_PROGRESS", "Datalake", "ETL", "TC-REG-007", sprint="Sprint-02",
                tags="cast,timestamp,bronze"),
        Anomaly("avg_amount inconsistency in Gold",
                "4 rows where avg_amount != total_amount/transaction_count (floating point rounding).",
                "LOW", "RESOLVED", "Datalake", "DATALAKE", "TC-GOLD-007", sprint="Sprint-02",
                tags="avg,float,gold"),
        Anomaly("INVALID_STATUS passes ETL check",
                "status=INVALID_STATUS not rejected by allowed values check. Regex updated needed.",
                "HIGH", "OPEN", "DataMart-Q1", "SQL", "DQ-016", sprint="Sprint-02",
                tags="status,allowed_values,sql"),
        Anomaly("Schema drift: new column _load_ts appeared",
                "Unexpected column _load_ts appeared in Silver after release v1.3. Not in reference schema.",
                "LOW", "WONT_FIX", "Datalake", "DATALAKE", "TC-COMP-001", sprint="Sprint-03",
                tags="schema,drift,column"),
    ]
    for a in samples:
        tracker.create(a)

    tracker.add_comment(samples[1].anomaly_id, "Imane M.",
                        "Confirmed root cause: ETL load step missing validation on amount sign.")
    tracker.add_comment(samples[3].anomaly_id, "Imane M.",
                        "Fix deployed in v1.2: added CANCELLED to exclusion list in bronze_to_silver().")
