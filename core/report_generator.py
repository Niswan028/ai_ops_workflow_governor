import json
from datetime import datetime


def generate_report(logs_filename: str, rules_filename: str, output_filename: str):
    with open(logs_filename) as f:
        import csv
        logs = list(csv.DictReader(f))

    with open(rules_filename) as f:
        rules = json.load(f)["governor_rules"]

    status_color = {"good": "#22c55e", "needs-improvement": "#f59e0b", "poor": "#ef4444"}

    rows_html = ""
    for r in logs:
        color = status_color.get(r["core_web_vitals_status"], "#gray")
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
        assets_str = ", ".join(assets) if assets else f"defer_delay={rule.get('defer_delay_ms', '')}ms"
        rules_html += f"""
        <div class="rule">
            <div class="rule-id">{rule['pattern_id']}</div>
            <div class="rule-action">Action: <strong>{rule['action_type']}</strong></div>
            <div>Assets: <code>{assets_str}</code></div>
            <div class="rule-gain">Estimated saving: {rule['estimated_load_time_reduction_ms']} ms</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI-Ops Workflow Governor — Report</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f8fafc; color: #1e293b; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .subtitle {{ color: #64748b; margin-bottom: 32px; font-size: 0.9rem; }}
  h2 {{ font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 32px; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  th {{ background: #1e293b; color: white; padding: 10px 14px; text-align: left; font-size: 0.85rem; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }}
  tr:last-child td {{ border-bottom: none; }}
  .rule {{ background: white; border-left: 4px solid #6366f1; padding: 14px 18px; margin-bottom: 12px; border-radius: 0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .rule-id {{ font-weight: bold; color: #6366f1; margin-bottom: 4px; }}
  .rule-action {{ margin-bottom: 4px; }}
  .rule-gain {{ color: #22c55e; font-weight: bold; margin-top: 6px; }}
  code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.85rem; }}
  .generated {{ color: #94a3b8; font-size: 0.8rem; margin-top: 40px; }}
</style>
</head>
<body>
<h1>AI-Ops Workflow Governor</h1>
<div class="subtitle">fitaichat.netlify.app — Performance Report</div>

<h2>Collected Metrics</h2>
<table>
  <thead>
    <tr><th>Timestamp</th><th>Page</th><th>TTFB</th><th>Load Time</th><th>Requests</th><th>CWV Status</th></tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>

<h2>Governor Rules ({len(rules)} recommendation{"s" if len(rules) != 1 else ""})</h2>
{rules_html if rules_html else '<p style="color:#94a3b8">No issues detected.</p>'}

<div class="generated">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
</body>
</html>"""

    with open(output_filename, "w") as f:
        f.write(html)

    print(f"[Report] HTML report written to {output_filename}")
