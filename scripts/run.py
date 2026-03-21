import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.governor import WorkflowGovernor

if __name__ == "__main__":
    log_file = "data/performance_logs.csv"
    out_file = "data/performance_rules.json"
    WorkflowGovernor().run(log_file, out_file)
