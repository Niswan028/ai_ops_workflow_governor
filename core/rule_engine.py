from typing import List, Dict


def make_prefetch_rule(assets: List[str], est_gain: float) -> Dict:
    return {
        "action_type": "prefetch_critical_assets",
        "critical_assets": assets,
        "estimated_load_time_reduction_ms": est_gain,
    }


def make_defer_rule(assets: List[str], est_gain: float) -> Dict:
    return {
        "action_type": "defer_non_critical_assets",
        "deferred_assets": assets,
        "estimated_load_time_reduction_ms": est_gain,
    }
