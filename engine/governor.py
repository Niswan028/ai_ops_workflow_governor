import json
from core.log_parser import parse_logs
from core.pattern_finder import find_slow_load_times, find_heavy_request_bursts
from core.rule_engine import make_prefetch_rule, make_defer_rule


class WorkflowGovernor:
    def run(self, log_filename: str, output_filename: str):
        logs = parse_logs(log_filename)
        rules = []

        if find_slow_load_times(logs):
            rules.append({
                "pattern_id": "fitbot_slow_load_time",
                **make_prefetch_rule(["/static/app.js", "/static/styles.css"], 400),
            })

        if find_heavy_request_bursts(logs):
            rules.append({
                "pattern_id": "chat_widget_burst",
                "action_type": "defer_chat_widget",
                "defer_delay_ms": 2000,
                "estimated_load_time_reduction_ms": 300,
            })

        with open(output_filename, "w") as f:
            json.dump({"governor_rules": rules}, f, indent=2)

        print(f"[Governor] {len(rules)} rule(s) written to {output_filename}")
