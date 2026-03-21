import json
from datetime import datetime, timezone
from typing import List, Dict

ALERT_LOG = "data/alerts.json"


def check_and_alert(logs: List[Dict], rules: List[Dict]):
    alerts = []

    for r in logs:
        if r["core_web_vitals_status"] == "poor":
            alerts.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "page": r["page_url"],
                "load_time_ms": r["load_time_ms"],
                "ttfb_ms": r["ttfb_ms"],
                "severity": "critical" if int(r["load_time_ms"]) > 3000 else "warning",
                "message": f"Page {r['page_url']} is POOR — load={r['load_time_ms']}ms, ttfb={r['ttfb_ms']}ms",
            })

    if alerts:
        # append to alert log
        try:
            with open(ALERT_LOG) as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        existing.extend(alerts)
        with open(ALERT_LOG, "w") as f:
            json.dump(existing, f, indent=2)

        print(f"\n[ALERT] {len(alerts)} alert(s) fired:")
        for a in alerts:
            tag = "CRITICAL" if a["severity"] == "critical" else "WARNING"
            print(f"  [{tag}] {a['message']}")
        print(f"[ALERT] Full alert log -> {ALERT_LOG}\n")
    else:
        print("[Alert] All pages healthy — no alerts.")

    return alerts
