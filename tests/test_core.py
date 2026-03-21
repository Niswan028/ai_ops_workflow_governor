import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.log_parser import parse_logs
from core.pattern_finder import find_slow_load_times, find_heavy_request_bursts, find_high_ttfb
from core.rule_engine import make_prefetch_rule, make_defer_rule
from core.alerting import check_and_alert


# --- log_parser ---

def test_parse_logs_returns_rows():
    logs = parse_logs("data/performance_logs.csv")
    assert len(logs) > 0
    assert "load_time_ms" in logs[0]

def test_parse_logs_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_logs("data/nonexistent.csv")


# --- pattern_finder ---

def test_find_slow_load_times_detects():
    logs = [{"load_time_ms": "2000"}, {"load_time_ms": "800"}]
    assert len(find_slow_load_times(logs)) == 1

def test_find_slow_load_times_empty():
    assert find_slow_load_times([]) == []

def test_find_slow_load_times_none_slow():
    logs = [{"load_time_ms": "500"}, {"load_time_ms": "900"}]
    assert find_slow_load_times(logs) == []

def test_find_heavy_request_bursts_detects():
    logs = [{"requests_count": "12"}, {"requests_count": "3"}]
    assert len(find_heavy_request_bursts(logs)) == 1

def test_find_heavy_request_bursts_empty():
    assert find_heavy_request_bursts([]) == []

def test_find_high_ttfb_detects():
    logs = [{"ttfb_ms": "700"}, {"ttfb_ms": "200"}]
    assert len(find_high_ttfb(logs)) == 1

def test_find_high_ttfb_empty():
    assert find_high_ttfb([]) == []


# --- rule_engine ---

def test_make_prefetch_rule():
    rule = make_prefetch_rule(["/app.js"], 400)
    assert rule["action_type"] == "prefetch_critical_assets"
    assert rule["critical_assets"] == ["/app.js"]
    assert rule["estimated_load_time_reduction_ms"] == 400

def test_make_defer_rule():
    rule = make_defer_rule(["/analytics.js"], 200)
    assert rule["action_type"] == "defer_non_critical_assets"
    assert rule["estimated_load_time_reduction_ms"] == 200

def test_make_prefetch_rule_empty_assets():
    rule = make_prefetch_rule([], 0)
    assert rule["critical_assets"] == []


# --- alerting ---

def test_alert_fires_on_poor():
    logs = [{"page_url": "/", "load_time_ms": "3500", "ttfb_ms": "700", "core_web_vitals_status": "poor"}]
    alerts = check_and_alert(logs, [])
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "critical"

def test_alert_warning_on_poor_under_3000():
    logs = [{"page_url": "/chat", "load_time_ms": "2800", "ttfb_ms": "500", "core_web_vitals_status": "poor"}]
    alerts = check_and_alert(logs, [])
    assert alerts[0]["severity"] == "warning"

def test_no_alert_on_good():
    logs = [{"page_url": "/", "load_time_ms": "800", "ttfb_ms": "200", "core_web_vitals_status": "good"}]
    alerts = check_and_alert(logs, [])
    assert alerts == []
