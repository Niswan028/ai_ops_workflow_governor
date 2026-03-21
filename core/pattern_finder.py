from typing import List, Dict


def find_slow_load_times(logs: List[Dict], threshold_ms: int = 1500) -> List[Dict]:
    return [r for r in logs if int(r["load_time_ms"]) > threshold_ms]


def find_heavy_request_bursts(
    logs: List[Dict], burst_window_ms: int = 300, min_burst_size: int = 10
) -> List[Dict]:
    return [r for r in logs if int(r["requests_count"]) >= min_burst_size]


def find_high_ttfb(logs: List[Dict], threshold_ms: int = 600) -> List[Dict]:
    return [r for r in logs if int(r["ttfb_ms"]) > threshold_ms]
