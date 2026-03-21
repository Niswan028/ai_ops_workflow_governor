import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.log_parser import parse_logs
from core.pattern_finder import find_slow_load_times, find_heavy_request_bursts
from core.rule_engine import make_prefetch_rule, make_defer_rule


def test_parse_logs():
    logs = parse_logs("data/performance_logs.csv")
    assert len(logs) == 5
    assert "load_time_ms" in logs[0]


def test_find_slow_load_times():
    logs = [{"load_time_ms": "2000"}, {"load_time_ms": "800"}]
    result = find_slow_load_times(logs)
    assert len(result) == 1


def test_find_heavy_request_bursts():
    logs = [{"requests_count": "12"}, {"requests_count": "3"}]
    result = find_heavy_request_bursts(logs)
    assert len(result) == 1


def test_make_prefetch_rule():
    rule = make_prefetch_rule(["/app.js"], 400)
    assert rule["action_type"] == "prefetch_critical_assets"
    assert rule["estimated_load_time_reduction_ms"] == 400


def test_make_defer_rule():
    rule = make_defer_rule(["/analytics.js"], 200)
    assert rule["action_type"] == "defer_non_critical_assets"
