import json
import csv
import os
from datetime import datetime


def generate_report(logs_filename: str, rules_filename: str, output_filename: str):
    with open(logs_filename) as f:
        logs = list(csv.DictReader(f))

    with open(rules_filename) as f:
        rules = json.load(f)["governor_rules"]

    history = _load_history()
    alerts = _load_alerts()

    status_color = {"good": "#22c55e", "needs-improvement": "#f59e0b", "poor": "#ef4444"}

    rows_html = ""
    for r in logs:
        color = status_color.get(r["core_web_vitals_status"], "#94a3b8")
        rows_html += f"""
        <tr>
            <td>{r['timestamp']}</td>
            <td>{r['page_url']}</td>
            <td>{r['ttfb_ms']} ms</td>
            <td>{r['load_time_ms']} ms</td>
            <td>{r['requests_count']}</td>
            <td><span style="color:{color};font-weight:bold">{r['core_web_vitals_status']}</span></td>
        </tr>"""

    rules_html = ""
    for rule in rules:
        assets = rule.get("critical_assets") or rule.get("deferred_assets", [])
        assets_str = ", ".join(assets) if assets else rule.get("recommendation", f"defer_delay={rule.get('defer_delay_ms','')}ms")
        rules_html += f"""
        <div class="rule">
            <div class="rule-id">{rule['pattern_id']}</div>
            <div class="rule-action">Action: <strong>{rule['action_type']}</strong></div>
            <div>Detail: <code>{assets_str}</code></div>
            <div class="rule-gain">Estimated saving: {rule['estimated_load_time_reduction_ms']} ms</div>
        </div>"""

    history_html = ""
    if history:
        for r in history[-20:]:  # last 20 entries
            color = status_color.get(r.get("core_web_vitals_status", ""), "#94a3b8")
            history_html += f"""
            <tr>
                <td>{r.get('timestamp','')[:19]}</td>
                <td>{r.get('page_url','')}</td>
                <td>{r.get('load_time_ms','')} ms</td>
                <td><span style="color:{color};font-weight:bold">{r.get('core_web_vitals_status','')}</span></td>
            </tr>"""
        history_section = f"""
        <h2>History (last {min(20, len(history))} runs)</h2>
        <table>
          <thead><tr><th>Timestamp</th><th>Page</th><th>Load Time</th><th>Status</th></tr></thead>
          <tbody>{history_html}</tbody>
        </table>"""
    else:
        history_section = ""

    alerts_html = ""
    if alerts:
        for a in alerts[-10:]:
            color = "#ef4444" if a.get("severity") == "critical" else "#f59e0b"
            alerts_html += f'<div class="alert" style="border-left-color:{color}"><strong>[{a["severity"].upper()}]</strong> {a["message"]} <span style="color:#94a3b8;font-size:0.8rem">— {a["timestamp"][:19]}</span></div>'
        alerts_section = f'<h2>Alerts (last {min(10, len(alerts))})</h2>{alerts_html}'
    else:
        alerts_section = '<h2>Alerts</h2><p style="color:#22c55e">No alerts — all pages healthy.</p>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI-Ops Workflow Governor — Report</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 20px; background: #f8fafc; color: #1e293b; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .subtitle {{ color: #64748b; margin-bottom: 32px; font-size: 0.9rem; }}
  h2 {{ font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 36px; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 8px; }}
  th {{ background: #1e293b; color: white; padding: 10px 14px; text-align: left; font-size: 0.85rem; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #f1f5f9; font-size: 0.88rem; }}
  tr:last-child td {{ border-bottom: none; }}
  .rule {{ background: white; border-left: 4px solid #6366f1; padding: 14px 18px; margin-bottom: 12px; border-radius: 0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .rule-id {{ font-weight: bold; color: #6366f1; margin-bottom: 4px; }}
  .rule-gain {{ color: #22c55e; font-weight: bold; margin-top: 6px; }}
  .alert {{ background: white; border-left: 4px solid #ef4444; padding: 10px 16px; margin-bottom: 8px; border-radius: 0 8px 8px 0; font-size: 0.9rem; }}
  code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.83rem; word-break: break-all; }}
  .generated {{ color: #94a3b8; font-size: 0.8rem; margin-top: 40px; }}
</style>
</head>
<body>
<h1>AI-Ops Workflow Governor</h1>
<div class="subtitle">fitaichat.netlify.app — Performance Report</div>

<h2>Latest Metrics</h2>
<table>
  <thead><tr><th>Timestamp</th><th>Page</th><th>TTFB</th><th>Load Time</th><th>Requests</th><th>CWV Status</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>

<h2>Governor Rules ({len(rules)} recommendation{"s" if len(rules) != 1 else ""})</h2>
{rules_html or '<p style="color:#94a3b8">No issues detected.</p>'}

{alerts_section}

{history_section}

<div class="generated">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
</body>
</html>"""

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Report] HTML report written to {output_filename}")


def _load_history():
    path = "data/performance_logs_history.csv"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))


def _load_alerts():
    path = "data/alerts.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
