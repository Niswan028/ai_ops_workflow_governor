# AI-Ops Workflow Governor
### for fitaichat.netlify.app — v1 Prototype

Reads website performance logs, detects patterns (slow loads, request bursts), and outputs actionable optimization rules as JSON.

---

## Structure

```
ai_ops_workflow_governor/
├── core/
│   ├── log_parser.py        # CSV log reader
│   ├── pattern_finder.py    # Slow load + burst detection
│   └── rule_engine.py       # Rule builders (prefetch / defer)
├── engine/
│   └── governor.py          # WorkflowGovernor orchestrator
├── data/
│   ├── performance_logs.csv # Input logs
│   └── performance_rules.json  # Output rules (generated)
├── scripts/
│   └── run.py               # Entry point
├── tests/
│   └── test_core.py
├── requirements.txt
└── README.md
```

## Quickstart

```bash
pip install -r requirements.txt
cd ai_ops_workflow_governor
python scripts/run.py
```

Output is written to `data/performance_rules.json`.

## Run Tests

```bash
pytest tests/
```

## Log Format

`data/performance_logs.csv` expects these columns:

| Column | Description |
|---|---|
| `timestamp` | ISO 8601 |
| `page_url` | Relative URL |
| `ttfb_ms` | Time to first byte (ms) |
| `load_time_ms` | Full page load time (ms) |
| `requests_count` | Number of HTTP requests |
| `core_web_vitals_status` | `good` / `needs-improvement` / `poor` |

## Extending to Other Sites

Replace `data/performance_logs.csv` with logs from any site. The governor is site-agnostic — only the `pattern_id` labels in `governor.py` are site-specific.
