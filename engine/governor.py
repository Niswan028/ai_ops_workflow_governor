import json
from core.log_parser import parse_logs
from core.pattern_finder import find_slow_load_times, find_heavy_request_bursts, find_high_ttfb
from core.rule_engine import make_prefetch_rule, make_defer_rule
from core.report_generator import generate_report
from core.alerting import check_and_alert


class WorkflowGovernor:
    def run(self, log_filename: str, output_filename: str):
        logs = parse_logs(log_filename)
        rules = []

        slow = find_slow_load_times(logs)
        if slow:
            # use real detected assets if available, else fallback
            assets = self._detected_assets(slow) or ["/static/app.js", "/static/styles.css"]
            rules.append({
                "pattern_id": "slow_load_time",
                **make_prefetch_rule(assets, 400),
            })

        if find_heavy_request_bursts(logs):
            rules.append({
                "pattern_id": "chat_widget_burst",
                "action_type": "defer_chat_widget",
                "defer_delay_ms": 2000,
                "estimated_load_time_reduction_ms": 300,
            })

        if find_high_ttfb(logs):
            rules.append({
                "pattern_id": "high_ttfb",
                "action_type": "enable_cdn_caching",
                "recommendation": "Enable CDN edge caching or move to a faster hosting region",
                "estimated_load_time_reduction_ms": 250,
            })

        with open(output_filename, "w") as f:
            json.dump({"governor_rules": rules}, f, indent=2)

        check_and_alert(logs, rules)

        report_file = output_filename.replace(".json", ".html")
        generate_report(log_filename, output_filename, report_file)

        print(f"[Governor] {len(rules)} rule(s) written to {output_filename}")

    def _detected_assets(self, logs):
        assets = []
        for r in logs:
            for asset in r.get("detected_assets", "").split("|"):
                if asset and asset not in assets:
                    assets.append(asset)
        return assets[:5]
