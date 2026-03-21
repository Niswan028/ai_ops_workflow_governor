# AI Ops Workflow Governor

Automated website performance auditing using real browser data — not synthetic scores.

This tool uses Playwright + Python to visit live websites, capture real network activity, detect performance issues, and generate actionable reports — fully automated via GitHub Actions.

---

## ⚙️ What It Does

A headless Chromium browser visits your site and collects:

* Page load time
* Time to First Byte (TTFB)
* Total network requests
* Real JS/CSS assets from the network tab

Then a rule engine analyzes the data and flags issues.

---

## 🚨 Detection Rules

| Rule           | Threshold     |
| -------------- | ------------- |
| Slow Load Time | > 1500ms      |
| Heavy Requests | > 10 requests |
| High TTFB      | > 600ms       |

---

## 📊 Output

* ✅ JSON alerts (machine-readable)
* 📄 HTML report (visual + history tracking)
* 🔁 Runs automatically via GitHub Actions

---

## 🧠 How It Works

Visit site → Capture network → Run detectors → Generate report → Trigger alerts

---

## 📸 Sample Report

(Add a screenshot here — this is very important)

---

## 🔍 Example Findings

Tested from India (cold loads):

* Reddit → ~731ms ✅
* Medium → ~783ms ✅
* dev.to → ~2271ms ⚠️
* civicpulse.in → ~6423ms 🔴

### Detected Issue (Example)

Next.js assets loading without prefetching:

```
/_next/static/chunks/*.js
/_next/static/chunks/*.css
```

### Suggested Fix

* Prefetch critical assets
* Enable CDN caching

Estimated improvement: ~650ms per page

---

## 💡 Why This Tool?

Most developers run Lighthouse once and move on.

This tool:

* Runs continuously (daily)
* Tracks performance trends
* Detects real issues from live traffic
* Suggests exactly what to fix

No manual checks required.

---

## 🧰 Tech Stack

* Python
* Playwright
* JSON / CSV
* GitHub Actions

Zero paid tools.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai_ops_workflow_governor.git
cd ai_ops_workflow_governor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 3. Run the audit

```bash
python main.py --url https://example.com
```

---

## 🔁 Automation (GitHub Actions)

The workflow runs daily and:

* Audits configured websites
* Stores results
* Generates reports automatically

Check `.github/workflows/` for setup.

---

## 📌 Roadmap

* [ ] Mobile performance simulation
* [ ] Lighthouse score integration
* [ ] Smarter (adaptive) thresholds
* [ ] Slack / Email alerts
* [ ] Dashboard UI

---

## 🤝 Contributing

Contributions are welcome.
Feel free to open issues or submit PRs.

---

## ⭐ Support

If you find this useful, consider giving it a star.

---

## 📬 Contact

Built by Niswan
(Open an issue or connect via GitHub)
